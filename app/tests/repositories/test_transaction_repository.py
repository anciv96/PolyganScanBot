import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.models.database import Base
from app.repositories.transaction import TransactionRepository
from app.models.transaction import Transaction


DATABASE_URL = "sqlite+aiosqlite:///:memory:"
async_engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_update_last_transaction():
    await engine()
    async with async_session() as session:
        transaction = {'hash': 'axn123'}

        repository = TransactionRepository(session)
        await repository.update_last_transaction(transaction)

        result = await session.execute(select(Transaction))
        saved_transaction = result.scalars().first()

        assert saved_transaction is not None
        assert saved_transaction.transaction_hash == "axn123"


@pytest.mark.asyncio
async def test_get_last_transaction():
    await engine()
    async with async_session() as session:
        transaction_hash = 'axn123'
        new_transaction = Transaction(
            transaction_hash=transaction_hash
        )
        session.add(new_transaction)
        await session.commit()

        repository = TransactionRepository(session)
        last_transaction = await repository.get_last_transaction()

        assert last_transaction is not None
        assert last_transaction.transaction_hash == transaction_hash
