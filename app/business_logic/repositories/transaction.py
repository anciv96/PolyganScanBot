from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import logger_setup
from app.business_logic.models.transaction import Transaction
from app.business_logic.repositories.decorators import session_start_decorator


logger = logger_setup.get_logger(__name__)


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @session_start_decorator
    async def update_last_transaction(self, token: str, transaction: dict[str, str]):
        transaction_hash = transaction.get('hash')

        saved_transaction = await self._get_saved_transaction(token)

        if saved_transaction:
            await self._update_transaction(saved_transaction, transaction_hash)
        else:
            await self._add_new_transaction(token, transaction_hash)

        await self.session.commit()

    async def _get_saved_transaction(self, token: str):
        try:
            row = await self.session.execute(
                select(Transaction).where(
                    Transaction.token == token
                )
            )
            result = row.scalars().first()
            return result
        except Exception as error:
            logger.error(error)

    async def _add_new_transaction(self, token, transaction_hash):
        try:
            new_transaction = Transaction(
                token=token,
                transaction_hash=transaction_hash,
            )
            self.session.add(new_transaction)
        except Exception as error:
            logger.error(error)

    async def _update_transaction(self, saved_transaction, transaction_hash):
        try:
            saved_transaction.transaction_hash = transaction_hash
        except Exception as error:
            logger.error(error)

    @session_start_decorator
    async def get_last_transaction(self, token):
        last_transaction = await self._get_saved_transaction(token)

        if not last_transaction:
            await self._add_new_transaction(token, 0)
            await self.session.flush()
            last_transaction = await self._get_saved_transaction(token)
            await self.session.commit()

        return last_transaction
