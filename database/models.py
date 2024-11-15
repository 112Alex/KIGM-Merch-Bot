from sqlalchemy import Text, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import date


class Base(DeclarativeBase):
    ...

class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_name: Mapped[str] = mapped_column(Text)
    event_date: Mapped[date] = mapped_column(Date)
    event_type: Mapped[str] = mapped_column(Text)