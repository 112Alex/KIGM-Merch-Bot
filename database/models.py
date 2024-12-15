from sqlalchemy import Column, Integer, BigInteger, Text, ForeignKey, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(Text, nullable=False)
    event_date = Column(Text, nullable=False)
    event_type = Column(Text, nullable=False)

    submissions = relationship("Submission", back_populates="event")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)
    group = Column(Text, nullable=False)
    score = Column(BigInteger)

    submissions = relationship("Submission", back_populates="user")
    bought_goods = relationship("BoughtGood", back_populates="user")


class Good(Base):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    price = Column(DECIMAL(8, 2), nullable=False)
    # icon_path = Column(Text, nullable=True)
    # description = Column(Text, nullable=True)

    bought_goods = relationship("BoughtGood", back_populates="good")


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subm_text = Column(Text, nullable=False)
    subm_date = Column(Text, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)

    event = relationship("Event", back_populates="submissions")
    user = relationship("User", back_populates="submissions")


class BoughtGood(Base):
    __tablename__ = 'bought_goods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    goods_id = Column(Integer, ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)

    user = relationship("User", back_populates="bought_goods")
    good = relationship("Good", back_populates="bought_goods")


