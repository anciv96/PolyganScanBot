from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Base(DeclarativeBase):
    pass


DATABASE_URL = 'sqlite+aiosqlite:///db.db'
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)
