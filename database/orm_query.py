import os
from sqlalchemy import func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from common import variables
from database.models import Event, Submission, User, Good, BoughtGood

from openpyxl import Workbook


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
async def orm_add_submission(session: AsyncSession, text: str, date: str, event_id: int, user_id: int):
    subm = Submission(
        subm_text = text,
        subm_date = date,
        event_id = event_id,
        user_id = user_id
    )
    session.add(subm)
    await session.commit()

#COMMENT Показать все заявки
async def orm_get_submissions(session: AsyncSession):
    query = select(Submission)
    results = await session.execute(query)
    return results.scalars().all()

#COMMENT Удалить заявку
async def orm_delete_subm(session: AsyncSession, subm_id):
    query = delete(Submission).where(Submission.id == subm_id)
    await session.execute(query)
    await session.commit()

#COMMENT Посмотреть ассортимент
async def orm_get_goods(session: AsyncSession):
    query = select(Good)
    results = await session.execute(query)
    return results.scalars().all()

#COMMENT Найти товар по id
async def orm_get_good(session: AsyncSession, good_id: int):
    query = select(Good).where(Good.id == good_id)
    result = await session.execute(query)
    return result.scalar()

#COMMENT Добавить купленный товар и списать баллы
async def orm_add_bought_good(session: AsyncSession, good_id: int, userId: int, amount: float):
    result = await session.execute(select(User).where(User.user_id == userId))
    user = result.scalar_one_or_none()

    if user is None:
        raise Exception("Пользователь не найден")

    if user.score < amount:
        raise Exception("Недостаточно баллов на счете")

    bought_good = BoughtGood(
        user_id=userId,
        goods_id=good_id
    )

    user.score -= amount

    session.add(bought_good)
    session.add(user)

    await session.commit()
    

#COMMENT Посмотреть купленные товары
async def orm_get_bought_goods(session: AsyncSession):
    stmt = select(
        BoughtGood.goods_id, 
        func.count(BoughtGood.id).label('count')
    ).group_by(BoughtGood.goods_id)

    result = await session.execute(stmt)
    counts = result.all()

    return counts

#COMMENT Добавить баллы
async def orm_add_score(session: AsyncSession, userId: int, score: int):
    query = select(User).where(User.user_id == userId)
    result = await session.execute(query)
    user = result.scalar()
    if user.score is None:
            user.score = 0
    user.score += score
    await session.commit()

#COMMENT Проверка на достаточное количество баллов при покупке
async def orm_check_score(session: AsyncSession, n: int, user_id: int):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    # Проверяем, существует ли пользователь
    if user is None:
        return f"User with id {user_id} not found."
    
    if user.score is None:
        return False
    else:
        return int(user.score) >= n
    
#COMMENT проверка на наличие товара у пользователя
async def orm_check_user_goods(session: AsyncSession, user_id: int, good_id: int):
    query = select(BoughtGood).where(
    BoughtGood.user_id == user_id,
    BoughtGood.goods_id == good_id
    )
    result = await session.execute(query)
    b_good = result.scalar_one_or_none()  # Это вернет первую строку или None

    if b_good is not None:
        # Если нашел товары, можно выполнить нужные действия
        return True
    
    return False  # Если нет товаров у пользователя
    
#COMMENT экспорт записей о купленном мерче в Xcel
async def export_goods_to_excel(session: AsyncSession):
    """Экспорт товаров в файл Excel."""

    goods = await session.execute(select(Good))  # Получаем все товары из базы данных
    bought_goods = await session.execute(select(BoughtGood))
    users = await session.execute(select(User))
    goods = goods.scalars().all()
    bought_goods = bought_goods.scalars().all()
    users = users.scalars().all()

    # Создаем новый Excel-файл
    workbook = Workbook()
    ws = workbook.active
    ws.title = "Goods"
        
    ws.append(['tg-id', 'название товара', 'имя', 'фамилия', 'группа', 'возраст'])
        
    for b_good in bought_goods:
        # Добавляем данные о товаре в Excel
        good = await session.execute(select(Good).where(Good.id == b_good.goods_id))
        good = good.scalar()
        user = await session.execute(select(User).where(User.user_id == b_good.user_id))
        user = user.scalar()
        ws.append([user.user_id, good.name, user.first_name, user.last_name, user.group, user.age])

        # Сохраняем файл
        workbook.save("bought_goods.xlsx")
        # print("Данные успешно экспортированы в goods.xlsx")
