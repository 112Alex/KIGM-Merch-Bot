from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Event, User


async def orm_add_event(session: AsyncSession, data: dict):
    event = Event(
        event_name=data["set_event_name"],
        event_date=data["set_event_date"],
        event_type=data["set_event_type"],
    )
    session.add(event)
    await session.commit()

async def orm_get_event(session: AsyncSession, event_id: int):
    query = select(Event).where(Event.id == event_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_events(session: AsyncSession):
    query = select(Event)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_update_event(session: AsyncSession, event_id: int, data):
    query = update(Event).where(Event.id == event_id).values(
        event_name=data["set_event_name"],
        event_date=data["set_event_date"],
        event_type=data["set_event_type"],)
    await session.execute(query)
    await session.commit()

async def orm_delete_event(session: AsyncSession, event_id: int):
    query = delete(Event).where(Event.id == event_id)
    await session.execute(query)
    await session.commit()

#COMMENT добавление пользователя
async def orm_add_user(session: AsyncSession, data: dict):
    event = User(
        name = data['name'],
        age = data['age'],
        group = data['group'],
    )
    session.add(event)
    await session.commit()