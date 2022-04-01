import pytest

from models import EmailConfirm, User, Vote, AuthLog, session


@pytest.fixture
def user():
    u = User()
    u.email = "a12345bc@example.com"
    u.enable = True
    u.blind_signature = "hoge"
    session.add(u)
    session.commit()

    yield u

    session.delete(u)
    session.commit()


@pytest.fixture
def email_confirm(user):
    c = EmailConfirm()
    c.password = "pwd"
    c.user_id = user._id
    session.add(c)
    session.commit()

    yield c

    session.delete(c)
    session.commit()


@pytest.fixture
def vote():
    v = Vote()
    v.vote1 = True
    v.vote2 = True
    v.vote3 = True
    v.vote4 = True
    v.vote5 = True
    v.vote6 = True
    v.vote7 = True
    v.free = "hoge"
    session.add(v)
    session.commit()

    yield v

    session.delete(v)
    session.commit()


@pytest.fixture
def auth_log(vote):
    a = AuthLog()
    a.signature = 'sig'
    a.unblind_signature = 'usig'
    a.pubkey = 'pkey'
    a.vote_id = vote._id
    session.add(a)
    session.commit()

    yield a

    session.delete(a)
    session.commit()


def test_email_validation(user):
    """Verify an email does not exist in user DB"""

    email = user.email

    assert User.exists(email)
    assert User.exists(email.upper())

    email2 = "b67890cd@example.com"
    assert not User.exists(email2)
    assert not User.exists(email2.upper())


def test_email_lookup_user(user, email_confirm):
    """Verify lookup email_confirm by user_id works"""

    user_id = user._id

    assert EmailConfirm.lookup_user(user_id) is not None
    assert EmailConfirm.lookup_user(user_id + 1) is None


def test_unblind_signature_exists(auth_log):
    """Verify unblind signature does not exist in DB"""

    unblind_signature = AuthLog.unblind_signature
    assert AuthLog.unblind_signature_exists(unblind_signature)

    unblind_signature2 = 'invalid' + auth_log.unblind_signature
    assert not AuthLog.unblind_signature_exists(unblind_signature2)


def test_password_exists(email_confirm):
    """Verify password does exist in DB"""
    password = email_confirm.password

    assert EmailConfirm.password_exists(password)
    assert not EmailConfirm.password_exists('invalid' + password)


def test_unbilnd_signature_exists(auth_log):
    """Verify password does not exist in DB"""
    unblind_signature = auth_log.unblind_signature

    assert AuthLog.unblind_signature_exists(unblind_signature)
    assert not AuthLog.unblind_signature_exists('invalid' + unblind_signature)
