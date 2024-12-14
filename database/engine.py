from os import getenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base, Good


engine = create_async_engine(getenv('KIGM_MERCH_DB'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

GOODS = {
    "Чехол для телефона": 450.00,
    "Термос": 540.00,
    "Кружка": 400.00,
    "Обложка на паспорт": 360.00,
    "Обложка на студенческий билет": 380.00,
    "Картхолдер": 340.00
}

async def add_goods():
    async with AsyncSession(engine) as session:
        async with session.begin():
            for name, price in GOODS.items():
                query = Good(name=name, price=price)
                session.add(query)
        await session.commit()