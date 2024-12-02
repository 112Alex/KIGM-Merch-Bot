from sqlalchemy import ForeignKey, Text, Date, BigInteger, Integer, SmallInteger, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from datetime import date


class Base(DeclarativeBase):
    ...


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_name: Mapped[str] = mapped_column(Text)
    event_date: Mapped[str] = mapped_column(Text)
    event_type: Mapped[str] = mapped_column(Text)


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    age: Mapped[int] = mapped_column(SmallInteger)
    group: Mapped[str] = mapped_column(Text)
    score: Mapped[int] = mapped_column(Integer)


class Submission(Base):
    __tablename__ = "submission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subm_text: Mapped[str] = mapped_column(Text)
    subm_date: Mapped[date] = mapped_column(Date)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    event: Mapped['Event'] = relationship(backref='submission')
    user: Mapped['User'] = relationship(backref='submission')


class Goods(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(8,2), nullable=False)
    icon_path: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class Buyed_Goods(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    goods_id: Mapped[int] = mapped_column(ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)

    buyed_goods: Mapped['Goods'] = relationship(backref='buyed_goods')
    




