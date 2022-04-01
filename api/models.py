import logging
from typing import Tuple

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.sql.sqltypes import Boolean


DATABASE_URL = "sqlite:///data.db"  # os.environ['DATABASE_URL']

ENGINE = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

session = scoped_session(
    sessionmaker(
        bind=ENGINE,
        autocommit=False,
    )
)


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    email_confirms = relationship("EmailConfirm", backref="users")
    blind_signatures = relationship("BlindSignature", backref="users")

    _id = Column('id', Integer, primary_key=True)
    email = Column('email', Text, unique=True)
    enable = Column('enable', Boolean, default=False)

    def get(id: int):
        return session.query(User).filter(
            User._id == id).first()

    def exists(email: str) -> bool:
        return User.lookup_email(email) is not None

    def lookup_email(email: str):
        return session.query(User).filter(
            User.email.ilike(email)).first()


class EmailConfirm(Base):
    __tablename__ = 'email_confirms'
    __table_args__ = {'extend_existing': True}

    _id = Column('id', Integer, primary_key=True)
    password = Column('password', Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    def password_exists(password: str) -> bool:
        return EmailConfirm.lookup_password(password) is not None

    def lookup_password(password: str):
        return session.query(EmailConfirm).filter(
            EmailConfirm.password == password).first()

    def lookup_user(user_id: int):
        return session.query(EmailConfirm).filter(
            EmailConfirm.user_id == user_id).first()


class BlindSignature(Base):
    __tablename__ = 'blind_signatures'
    _id = Column('id', Integer, primary_key=True)
    blind_signature = Column('blind_signature', Text)
    user_id = Column(Integer, ForeignKey('users.id'))


class Vote(Base):
    __tablename__ = 'votes'
    __table_args__ = {'extend_existing': True}
    auth_logs = relationship("AuthLog", backref="votes")

    _id = Column('id', Integer, primary_key=True)
    vote1 = Column('vote1', Boolean)
    vote2 = Column('vote2', Boolean)
    vote3 = Column('vote3', Boolean)
    vote4 = Column('vote4', Boolean)
    vote5 = Column('vote5', Boolean)
    vote6 = Column('vote6', Boolean)
    vote7 = Column('vote7', Boolean)
    vote8 = Column('vote8', Boolean)
    vote9 = Column('vote9', Boolean)
    vote10 = Column('vote10', Boolean)
    vote11 = Column('vote11', Boolean)
    vote12 = Column('vote12', Boolean)
    vote13 = Column('vote13', Boolean)
    free = Column('free', Text)


class AuthLog(Base):
    __tablename__ = 'auth_logs'
    __table_args__ = {'extend_existing': True}

    _id = Column('id', Integer, primary_key=True)
    signature = Column('signature', Text)
    unblind_signature = Column('unblind_signature', Text)
    pubkey = Column('pubkey', Text)
    vote_id = Column(Integer, ForeignKey('votes.id'))

    def unblind_signature_exists(unblind_signature: str) -> bool:
        return AuthLog.lookup_unblind_signature(unblind_signature) is not None

    def lookup_unblind_signature(unblind_signature: str):
        return session.query(AuthLog).filter(
            AuthLog.unblind_signature == unblind_signature).first()


def DANGER_erase_db():
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        logging.warning('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


# todo: rename
class VoteAndAuthlogRepository:
    def gen_or_find_by_pubkey(pubkey: str) -> Tuple[Vote, AuthLog]:
        authlog = session.query(AuthLog).filter(
            AuthLog.pubkey == pubkey).first()

        if authlog:
            vote = session.query(Vote).filter(
                Vote._id == authlog.vote_id).first()
        else:
            vote = Vote()
            authlog = AuthLog()

        return (vote, authlog)

    def add_and_commit(vote, authlog):
        session.add(vote)
        session.commit()

        authlog.vote_id = vote._id
        session.add(authlog)

        session.commit()


Base.metadata.create_all(ENGINE)

if __name__ == '__main__':
    user = User()
    user.email = 'b'
    user.blind_signature = 'c'

    vote = Vote()
    vote.vote1 = True
    vote.vote2 = True
    vote.vote3 = True
    vote.vote4 = True
    vote.vote5 = True
    vote.vote6 = True
    vote.vote7 = True
    vote.free = 'b'

    log = AuthLog()
    log.signature = "aaa"
    log.pubkey = "bbb"
    log.unblind_signature = "ccc"
    log.vote_id = vote._id

    session.add(user)
    session.add(vote)
    session.add(log)
    session.commit()
