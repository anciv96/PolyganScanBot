import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import async_session, Base, engine
from app.models.transaction import Transaction
from app.repositories.decorators import session_start_decorator


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @session_start_decorator
    async def update_last_transaction(self, transaction: dict[str, str]):
        transaction_hash = transaction.get('hash')
        timestamp = transaction.get('timeStamp')

        saved_transaction = await self._get_saved_transaction()

        if not saved_transaction:
            await self._add_new_transaction(transaction_hash, timestamp)
        else:
            await self._update_transaction(saved_transaction, transaction_hash, timestamp)

        await self.session.commit()

    async def _get_saved_transaction(self):
        result = await self.session.execute(
            select(Transaction)
        )
        return result.scalars().first()

    async def _add_new_transaction(self, transaction_hash, timestamp):
        new_transaction = Transaction(
            transaction_hash=transaction_hash,
            timestamp=timestamp,
        )
        self.session.add(new_transaction)

    async def _update_transaction(self, saved_transaction, transaction_hash, timestamp):
        saved_transaction.transaction_hash = transaction_hash
        saved_transaction.timestamp = timestamp

    @session_start_decorator
    async def get_last_transaction(self):
        last_transaction = await self._get_saved_transaction()

        if last_transaction:
            return last_transaction
        else:
            await self._add_new_transaction(0, 0)
            await self.session.commit()
            return await self.get_last_transaction()







async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def main():
    await init_db()
    async with async_session() as session:
        repository = TransactionRepository(session)
        a = await repository.get_last_transaction()
        print(a.timestamp)


if __name__ == '__main__':
    asyncio.run(main())
