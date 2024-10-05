import asyncio

from app.models.database import engine, Base, async_session
from app.repositories.transaction import TransactionRepository
from app.config import TOKENS
from app.services.scrapers.polygonscan.polygonscan_scraper import PolygonScanScraper
from app.services.scrapers.polygonscan.strategies.transaction_fetch_strategy import TransactionFetchStrategy
from app.models.transaction import Transaction
from app.models.our_token import OurToken


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def main():
    await init_db()
    async with async_session() as session:
        repository = TransactionRepository(session)
        transaction_strategy = TransactionFetchStrategy()
        transaction_scraper = PolygonScanScraper(TOKENS, repository, transaction_strategy)
        transactions = await transaction_scraper.execute()

        for i, transaction in enumerate(transactions):
            print(i, transaction)


if __name__ == "__main__":
    asyncio.run(main())
