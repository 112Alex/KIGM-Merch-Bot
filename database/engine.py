from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.future import select
from sqlalchemy import func

from database.models import Base, Good
from database.seeds import add_initial_goods # Import add_initial_goods


engine = create_async_engine(getenv('KIGM_MERCH_DB'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        await add_initial_goods(session) # Call the new function




