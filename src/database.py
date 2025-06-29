from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import asyncio
from sqlalchemy import URL

from src.config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST
from src.models import Base


# con_url = URL.create(
#     "postgresql+asyncpg",
#     username=DB_USERNAME,
#     password=DB_PASSWORD,
#     host=DB_HOST,
#     database=DB_NAME
# )
con_url = "sqlite+aiosqlite:///news.db"
engine = create_async_engine(con_url)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with session_factory() as session:
        yield session

    
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        

@asynccontextmanager
async def session_scope(): 
    session = session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(init_db())
