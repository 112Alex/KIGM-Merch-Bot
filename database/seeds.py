from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.models import Good

GOODS = {
    "Чехол для телефона": 450.00,
    "Термос": 540.00,
    "Кружка": 400.00,
    "Обложка на паспорт": 360.00,
    "Обложка на студенческий билет": 380.00,
    "Картхолдер": 340.00
}

async def add_initial_goods(session: AsyncSession):
    # Check if the goods table is empty
    result = await session.execute(select(func.count()).select_from(Good))
    if result.scalar() == 0:
        for name, price in GOODS.items():
            session.add(Good(name=name, price=price))
        await session.commit()
