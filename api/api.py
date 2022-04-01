from email import message
from flask import Flask, request, render_template, jsonify
from sqlalchemy.sql.expression import false
from send_email import send_confirm_email, send_all_blind_signature_email, send_registration_email, GMailError

from signer import sign, verify
from models import User, Vote, AuthLog, BlindSignature, EmailConfirm, session, DANGER_erase_db, VoteAndAuthlogRepository
from flask import Flask, request, render_template
import os
import logging
import json
import secrets
import re
import cerberus

import base64
import binascii
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

VOTES_LENGTH = 13

VOTE_SCHEMA = {
    'votes': {
        'type': 'list',
        'required': True,
        'minlength': VOTES_LENGTH,
        'maxlength': VOTES_LENGTH,
        'schema': {
            'type': 'boolean',
        },
    }
}


PUBKEY = os.environ['PUBKEY']
PRIVKEY = os.environ['PRIVKEY']
INCUBATOR_PASS = os.environ['INCUBATOR_PASS']
# LOG_FILE = os.environ.get('LOG_FILE') or 'data/api.log'

app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True

app.logger.setLevel(logging.DEBUG)
# log_handler = logging.FileHandler(LOG_FILE)
# log_handler.setLevel(logging.DEBUG)
# app.logger.addHandler(log_handler)

HTTP_OK = 200
HTTP_BADREQUEST = 400
HTTP_INTERNAL_SERVER_ERROR = 500


GMAIL_ASK_ADMIN_MSG = 'メールを送信する際にエラーが発生しました。サイト管理者に問い合わせてください。 We had some troubles to send an email to you. Please contact the administrator.'
GMAIL_ASK_ADMIN_CODE = 1


@app.route("/api/pubkey", methods=['GET'])
def pubkey():
    return PUBKEY


"""
@app.route("/incubator/api/send_email", methods=['POST'])
def incubator_send_email():
    try:
        send_all_blind_signature_email()
    except GMailError as e:
        return jsonify({'result': False, 'error': GMAIL_ASK_ADMIN_MSG, 'error_code': GMAIL_ASK_ADMIN_CODE}), HTTP_INTERNAL_SERVER_ERROR

    return jsonify({'result': True})
"""


"""
@app.route("/incubator/api/erase_db", methods=['POST'])
def incubator_erase_db():
    if request.form['confirm'] == 'OK':
        DANGER_erase_db()
        return 'done'
    else:
        return 'ignored'
"""

@app.route("/api/register", methods=['POST'])
def post_register():
    """ To disable API again, uncomment these lines.
        DON'T FORGET TO DISABLE WEB REGISTRATION BUTTON TOO. (see: /app/src/pages/register.vue)
    return jsonify({
        'error_code': 99,
        'error': '事前登録は一時的に停止されています。詳しくは、続くリンクを参照してください。 The registeration is paused.  For more information, please see the following website. '
    }), HTTP_BADREQUEST
    """

    regex = r'\A^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]Z'
    pattern = re.compile(regex)

    email = request.form["email"].lower()

    if not pattern.match(email):
        return 'email not correct'

    if User.exists(email):
        app.logger.debug("req: %s", User.lookup_email(email))
        return jsonify({'result': False, 'error': 'email already registered', 'error_code': 101}), HTTP_BADREQUEST

    password = secrets.token_urlsafe()

    try:
        send_confirm_email(email, password)
    except GMailError as e:
        return jsonify({'result': False, 'error': GMAIL_ASK_ADMIN_MSG, 'error_code': GMAIL_ASK_ADMIN_CODE}), HTTP_INTERNAL_SERVER_ERROR

    user = User()
    user.email = email
    user.enable = False

    session.add(user)
    session.commit()

    email_confirm = EmailConfirm()
    email_confirm.password = password
    email_confirm.user_id = user._id

    session.add(email_confirm)
    session.commit()

    return jsonify({'result': True})



@app.route("/api/confirm", methods=['POST'])
def post_confirm():
    password = request.form["password"]
    blind_digest = request.form["blind_digest"]
    regenerate = request.form["regenerate"]

    if not EmailConfirm.password_exists(password):
        return jsonify({'result': False, 'error': '認証情報が間違っています', 'error_code': 201}), HTTP_BADREQUEST

    app.logger.debug("blind_digest: %s", blind_digest)

    email_confirm = EmailConfirm.lookup_password(password)

    user = User.get(email_confirm.user_id)
    if user.enable and not regenerate == 'true':
        return jsonify({'result': False, 'error': '鍵の再生成', 'error_code': 101}), HTTP_BADREQUEST

    user.enable = True

    text_blind_signature = sign(blind_digest, PRIVKEY)

    blind_signature = BlindSignature()
    blind_signature.blind_signature = text_blind_signature
    blind_signature.user_id = user._id

    session.add(blind_signature)
    session.commit()

    try:
        send_registration_email(user.email)
    except GMailError as e:
        return jsonify({'result': False, 'error': GMAIL_ASK_ADMIN_MSG, 'error_code': GMAIL_ASK_ADMIN_CODE}), HTTP_INTERNAL_SERVER_ERROR

    return jsonify({'result': True})


@app.route("/api/vote", methods=['POST'])
def post_vote():
    # get post data
    text_message = request.form["message"]
    free_description = request.form["free_description"]
    pubkey = request.form["pubkey"]
    unblind_signature = request.form["unblind_signature"]
    signature = request.form["signature"]

    # varidate and cast to dict
    message = json.loads(text_message)
    vote_validator = cerberus.Validator(VOTE_SCHEMA)
    if not vote_validator.validate(message):
        return json.dumps(vote_validator.errors)

    # decode pubkey and signature
    try:
        decoded_pubkey = base64.b64decode(pubkey)
        decoded_signature = base64.b64decode(signature)
    except binascii.Error as e:
        return jsonify({'result': False, 'error': 'data you sent have an invalid format', 'error_code': 301}), HTTP_BADREQUEST

    # import rsa key and generate hash
    rsa_pubkey = RSA.import_key(decoded_pubkey)
    hash = SHA256.new(text_message.encode('utf-8'))

    # for debug
    app.logger.debug("pubkey: %s", pubkey)
    app.logger.debug("unblind_signature: %s", unblind_signature)
    app.logger.debug("signature: %s", signature)
    app.logger.debug("votes: %s", message['votes'])

    # verify rsa signature
    try:
        pkcs1_15.new(rsa_pubkey).verify(hash, decoded_signature)
    except ValueError as e:
        app.logger.debug("pubkey: '%s'", pubkey)
        app.logger.debug("hash: '%s'", hash)
        app.logger.debug("decoded_signature: '%s'", decoded_signature)
        return jsonify({'result': False, 'error': 'invalid RSA signature and pubkey pair', 'error_code': 302}), HTTP_BADREQUEST

    # verify blind signature
    result = verify(pubkey, unblind_signature, PUBKEY)
    if not result:
        return jsonify({'result': False, 'error': 'signature verification failed', 'error_code': 304}), HTTP_BADREQUEST

    vote, authlog = VoteAndAuthlogRepository.gen_or_find_by_pubkey(pubkey)
    print(vote.free)

    '''
    for i in range(VOTES_LENGTH):
        vote.__dict__[f'vote{i + 1}'] = message['votes'][i]
    '''

    # chikara koso power
    if True:
        vote.vote1 = message['votes'][0]
        vote.vote2 = message['votes'][1]
        vote.vote3 = message['votes'][2]
        vote.vote4 = message['votes'][3]
        vote.vote5 = message['votes'][4]
        vote.vote6 = message['votes'][5]
        vote.vote7 = message['votes'][6]
        vote.vote8 = message['votes'][7]
        vote.vote9 = message['votes'][8]
        vote.vote10 = message['votes'][9]
        vote.vote11 = message['votes'][10]
        vote.vote12 = message['votes'][11]
        vote.vote13 = message['votes'][12]
        #vote.vote14 = message['votes'][14]
        #vote.vote15 = message['votes'][15]

    vote.free = free_description

    print("vote:",  vote)

    authlog.signature = signature
    authlog.unblind_signature = unblind_signature
    authlog.pubkey = pubkey
    authlog.vote_id = vote._id

    VoteAndAuthlogRepository.add_and_commit(vote, authlog)

    return jsonify({'result': True})


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        threaded=False)
