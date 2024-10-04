import asyncio
from abc import ABC, abstractmethod
from typing import Any

import aiohttp

from app.repositories.transaction import TransactionRepository
from app.config import TOKENS, POLYGON_SCAN_KEY


class Scraper(ABC):
    @abstractmethod
    async def get_transactions(self):
        pass


class PolygonScanScraper(Scraper):
    BASE_URL = 'https://api.polygonscan.com/api'

    def __init__(self, tokens: list[str], repository: TransactionRepository):
        self.tokens = tokens
        self.repository = repository

    async def get_transactions(self) -> list[dict[str, Any]]:
        all_transactions = await self._fetch_transactions()

        for new_transaction in all_transactions:
            print(new_transaction)
        return all_transactions

    async def _fetch_transactions(self, page=1) -> list[dict[str, str]]:
        async with aiohttp.ClientSession() as session:
            result = []
            for token in self.tokens:
                params = {
                    "module": "account",
                    "action": "txlist",
                    "address": token,
                    "startblock": 0,
                    "endblock": 99999999,
                    "page": page,
                    "offset": 2,
                    "sort": "desc",
                    "apikey": POLYGON_SCAN_KEY,
                }
                async with session.get(self.BASE_URL, params=params, ssl=False) as response:
                    data = await response.json()
                    if data.get("status") == "1":
                        for transaction in data.get("result", []):
                            if await self._transaction_is_new(transaction):
                                result.append(transaction)
                        else:
                            if len(result) == 0:
                                result.append(await self._fetch_transactions(page=page+1))

            return result

    async def _transaction_is_new(self, transaction: dict[str, str], test) -> bool:
        last_transaction = await self.repository.get_last_transaction()
        if transaction != last_transaction and last_transaction < int(transaction.get('timeStamp')):
            return True
        else:
            await self.repository.update_last_transaction(transaction)
            return False


if __name__ == '__main__':
    repository = TransactionRepository()
    scraper = PolygonScanScraper(TOKENS, repository)
    asyncio.run(scraper.get_transactions())
