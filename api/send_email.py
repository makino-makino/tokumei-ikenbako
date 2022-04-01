import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from models import BlindSignature, session, User, EmailConfirm
import time
import os

DOMAIN = os.environ.get('DEPLOY_HOST') or 'localhost'
SMTP_SERVER = "smtp.gmail.com"

logging.basicConfig(level=logging.DEBUG)

CONFIRM_EMAIL_TEXT = """

<a href="{url}">{url}</a>

<br><br>
"""

COMPLETE_EMAIL_TEXT = """
<br><br>
"""

VOTE_EMAIL_TEXT = """
<a href="{url}">{url}</a>
"""

try:
    EMAIL_FROM = os.environ['EMAIL_FROM']
    PASSWORD = os.environ['PASSWORD']
    TIME = os.environ['TIME']
except KeyError as e:
    logging.error(
        'failed to fetch environment variable. You may need to edit .env?: %s', e)
    raise e

logging.debug("email from: `%s`", EMAIL_FROM)
logging.debug("password : `%s`", PASSWORD)
logging.debug("time : `%s`", TIME)


def send_confirm_email(mail_to, token):
    subject = "subject"

    body = CONFIRM_EMAIL_TEXT.format(
        url=f"https://{DOMAIN}/confirm#{token}")

    send(subject, mail_to, body)


def send_registration_email(mail_to):
    subject = "subject"
    body = COMPLETE_EMAIL_TEXT

    send(subject, mail_to, body)


def send_blind_signature_email(mail_to, signature):
    subject = "subject"

    body = VOTE_EMAIL_TEXT.format(
        url=f"https://{DOMAIN}/vote#{signature}")

    send(subject, mail_to, body)


def send_all_confirm_email(interval=2):
    users = session.query(User).all()

    for user in users:
        if user.enable:
            continue

        email_confirm = EmailConfirm.lookup_user(user._id)

        logging.debug("email: %s", user.email)
        logging.debug("blind_signature: %s", email_confirm.password)

        time.sleep(interval)
        send_confirm_email(user.email, email_confirm.password)


def send_all_blind_signature_email(interval=2):
    users = session.query(User).all()

    for user in users:
        if not user.enable:
            continue

        blind_signature = session.query(BlindSignature).filter(
            BlindSignature.user_id == user._id).last()

        logging.debug("email: %s", user.email)
        logging.debug("blind_signature: %s", blind_signature.blind_signature)

        time.sleep(interval)
        send_blind_signature_email(user.email, blind_signature.blind_signature)


def send(subject, to, body, from_=EMAIL_FROM):
    msg = MIMEText(body, "html")

    msg["Subject"] = subject
    msg["To"] = to
    msg["From"] = from_

    server = smtplib.SMTP_SSL(SMTP_SERVER, 465,
                              context=ssl.create_default_context())

    try:
        server.login(EMAIL_FROM, PASSWORD)
        server.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        raise GMailError(e)

    logging.info('sent email')
    logging.info('\tTo:\t%s', to)
    logging.info('\tSubject:\t%s', subject)
    logging.info('%s', body)


class GMailError(smtplib.SMTPAuthenticationError):
    def __init__(self, auth_error: smtplib.SMTPAuthenticationError):
        if "google" in str(auth_error):
            self.msg = 'failed to authenticate gmail account: %s' % auth_error
            logging.error('GMailError: %s', self.msg)
        else:
            self.msg = str(auth_error)

        self.base = auth_error

    def __str__(self):
        return self.msg


if __name__ == '__main__':
    interval_slowly = 300  # 5 min.
    interval_midium = 60  # 1 min.
    interval_early = 2  # 2 sec.

    send_all_blind_signature_email(5)
    # send_all_blind_signature_email(interval_slowly)
