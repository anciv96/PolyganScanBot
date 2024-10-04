import asyncio
from abc import ABC, abstractmethod
from typing import Any, List, Dict

import aiohttp

from app.models.database import engine, Base, async_session
from app.repositories.transaction import TransactionRepository
from app.config import TOKENS, POLYGON_SCAN_KEY


class Scraper(ABC):
    @abstractmethod
    async def get_transactions(self):
        pass


class PolygonScanScraper(Scraper):
    BASE_URL = 'https://api.polygonscan.com/api'

    def __init__(self, tokens: List[str], repository: TransactionRepository):
        self.tokens = tokens
        self.repository = repository

    async def get_transactions(self) -> List[dict[str, Any]]:
        """Получить все транзакции для указанных токенов."""
        all_transactions = await self._fetch_all_transactions()
        return all_transactions

    async def _fetch_all_transactions(self) -> List[dict[str, Any]]:
        """Рекурсивно загружает все транзакции по токенам."""
        transactions = []
        for token in self.tokens:
            token_transactions = await self._fetch_token_transactions(token)
            transactions.extend(token_transactions)

        if transactions:
            await self.repository.update_last_transaction(transactions[0])

        return transactions

    async def _fetch_token_transactions(self, token: str, page: int = 1) -> List[dict[str, Any]]:
        """Загружает транзакции для конкретного токена с учётом фильтрации."""
        result = []
        async with aiohttp.ClientSession() as session:
            for _ in range(20):
                response_data = await self._fetch_transactions_page(session, token, page)
                transactions = response_data.get("result", [])

                if response_data.get("status") != "1" or not transactions:
                    break

                new_transactions = await self._filter_new_transactions(transactions)
                result.extend(new_transactions)

                if len(new_transactions) < len(transactions):
                    break

                page += 1

        return result

    async def _fetch_transactions_page(self, session: aiohttp.ClientSession, token: str, page: int) -> dict[str, Any]:
        """Получает одну страницу транзакций с PolygonScan API."""
        params = {
            "module": "account",
            "action": "txlist",
            "address": token,
            "startblock": 0,
            "endblock": 99999999,
            "page": page,
            "offset": 10,
            "sort": "desc",
            "apikey": POLYGON_SCAN_KEY,
        }
        async with session.get(self.BASE_URL, params=params, ssl=False) as response:
            return await response.json()

    async def _filter_new_transactions(self, transactions: List[dict[str, Any]]) -> List[dict[str, Any]]:
        """Фильтрует только новые транзакции, которые еще не были сохранены."""
        result = []
        for transaction in transactions:
            if await self._transaction_is_new(transaction):
                result.append(transaction)
            else:
                # Если встречаем старую транзакцию, считаем, что дальше пойдут только старые
                break

        return result

    async def _transaction_is_new(self, transaction: dict[str, Any]) -> bool:
        """Проверяет, является ли транзакция новой по сравнению с последней сохраненной."""
        last_transaction = await self.repository.get_last_transaction()
        return transaction.get('hash') != last_transaction.transaction_hash


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def main():
    await init_db()
    async with async_session() as session:
        repository = TransactionRepository(session)
        scraper = PolygonScanScraper(TOKENS, repository)
        transactions = await scraper.get_transactions()

if __name__ == '__main__':
    asyncio.run(main())
