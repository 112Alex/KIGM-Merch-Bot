from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Event, Submission, User


async def orm_add_event(session: AsyncSession, data: dict):
    event = Event(
        event_name=data["set_event_name"],
        event_date=data["set_event_date"],
        event_type=data["set_event_type"],
    )
    session.add(event)
    await session.commit()

#COMMENT Поиск ивента по event_id
async def orm_get_event(session: AsyncSession, event_id: int):
    query = select(Event).where(Event.id == event_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_events(session: AsyncSession):
    query = select(Event)
    result = await session.execute(query)
    return result.scalars().all()

#COMMENT Изменить данные ивента
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


#COMMENT Добавляем пользователя в БД
async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    group: str | None = None,
    age: int | None = None
):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id, first_name=first_name, last_name=last_name, group=group, age=age)
        )
        await session.commit()

#COMMENT ищем пользователя по user_id
async def find_by_user_id(session: AsyncSession, user_id: int):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()

#COMMENT отображение кол-ва баллов
async def orm_show_score(session: AsyncSession, user_id: int):
    query = select(User.score).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()

#COMMENT создание заявки
async def orm_add_submission(session: AsyncSession, text: str, date, event_id: int, user_id: int):
    subm = Submission(
        subm_text = text,
        subm_date = date,
        event_id = event_id,
        user_id = user_id
    )
    session.add(subm)
    await session.commit()