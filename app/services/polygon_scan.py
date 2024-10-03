from abc import ABC, abstractmethod

from app.repositories.transaction import TransactionRepository


class Scraper(ABC):
    @abstractmethod
    async def get_transactions(self):
        pass


class PolygonScanScraper(Scraper):
    def __init__(self, tokens: list[str], repository: TransactionRepository):
        self.tokens = tokens
        self.repository = repository

    async def get_transactions(self):
        all_transactions = await self._fetch_transactions(self.tokens)
        new_transactions = await self._filter_new_transactions(all_transactions)

        return new_transactions

    async def _fetch_transactions(self, tokens: list[str]) -> list[dict[str, str]]:
        pass

    async def _filter_new_transactions(self, transactions: list[dict[str, str]]):
        result = []
        last_transaction = await self.repository.get_last_transaction()
        for transaction in transactions:
            if transaction != last_transaction and last_transaction.timestamp < transaction.timestamp:
                result.append(transaction)
            else:
                break

        return result
