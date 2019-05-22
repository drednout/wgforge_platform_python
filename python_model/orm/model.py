from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, BigInteger, Text,
    DateTime, text,
    UniqueConstraint
)

Base = declarative_base()


class AsDictMixin(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Money(Base, AsDictMixin):
    __tablename__ = 'money'
    __table_args__ = (
        UniqueConstraint('player_id', 'currency_code'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('money_id_seq'::regclass)"))
    player_id = Column(BigInteger, nullable=False)
    currency_code = Column(Text, nullable=False)
    amount = Column(BigInteger, nullable=False)
    created = Column(DateTime, server_default=text("timezone('UTC'::text, now())"))
    updated = Column(DateTime, server_default=text("timezone('UTC'::text, now())"))



class Player(Base, AsDictMixin):
    __tablename__ = 'player'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('player_id_seq'::regclass)"))
    nickname = Column(Text, nullable=False, unique=True)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    created = Column(DateTime, server_default=text("timezone('UTC'::text, now())"))
    updated = Column(DateTime, server_default=text("timezone('UTC'::text, now())"))
