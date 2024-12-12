from sqlalchemy import Column, Integer, BigInteger, String, Text, Date, ForeignKey, DECIMAL, func
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
    score = Column(Integer)

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
    subm_date = Column(Date, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)

    event = relationship("Event", back_populates="submissions")
    user = relationship("User", back_populates="submissions")


class BoughtGood(Base):
    __tablename__ = 'buyed_goods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    goods_id = Column(Integer, ForeignKey('goods.id'), nullable=False)

    user = relationship("User", back_populates="bought_goods")
    good = relationship("Good", back_populates="bought_goods")




#NOTE старая версия модели (не работает)
# class Base(DeclarativeBase):
#     ...
# class Event(Base):
#     __tablename__ = 'event'
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     event_name: Mapped[str] = mapped_column(Text)
#     event_date: Mapped[str] = mapped_column(Text)
#     event_type: Mapped[str] = mapped_column(Text)
# class User(Base):
#     __tablename__ = "user"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
#     name: Mapped[str] = mapped_column(Text)
#     age: Mapped[int] = mapped_column(SmallInteger)
#     group: Mapped[str] = mapped_column(Text)
#     score: Mapped[int] = mapped_column(Integer)
# class Submission(Base):
#     __tablename__ = "submission"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     subm_text: Mapped[str] = mapped_column(Text)
#     subm_date: Mapped[date] = mapped_column(Date)
#     event_id: Mapped[int] = mapped_column(ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
#     event: Mapped['Event'] = relationship(backref='submission')
#     user: Mapped['User'] = relationship(backref='submission')
# class Goods(Base):
#     __tablename__ = "goods"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(Text)
#     price: Mapped[float] = mapped_column(Numeric(8,2), nullable=False)
#     icon_path: Mapped[str] = mapped_column(Text)
#     description: Mapped[str] = mapped_column(Text)
# class Buyed_Goods(Base):
#     __tablename__ = "buyed_goods"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
#     goods_id: Mapped[int] = mapped_column(ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
#     goods: Mapped['Goods'] = relationship(backref='buyed_goods')
#     user_id: Mapped['User'] = relationship(backref='buyed_goods')






