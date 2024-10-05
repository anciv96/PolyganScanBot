from typing import Any

import aiohttp

from app.config import POLYGON_SCAN_KEY
from app.repositories.transaction import TransactionRepository
from app.services.scrapers.polygonscan.polygonscan_scraper import PolygonScanScraper
from app.services.scrapers.polygonscan.base_strategy import PolygonScanStrategy


class TransactionFetchStrategy(PolygonScanStrategy):

    async def fetch(self, tokens: list[str], repository: TransactionRepository) -> list[dict[str, Any]]:
        """
        Fetch transactions for the provided tokens.

        Args:
            tokens (List[str]): A list of token addresses to fetch transactions for.
            repository (TransactionRepository): A repository to manage transactions.

        Returns:
            List[dict[str, Any]]: A list of dictionaries containing the transaction data.
        """
        self.tokens = tokens
        self.repository = repository

        all_transactions = await self._fetch_all_transactions()
        return all_transactions

    async def _fetch_all_transactions(self) -> list[dict[str, Any]]:
        """Recursively loads all token transactions"""
        transactions = []
        for token in self.tokens:
            token_transactions = await self._fetch_token_transactions(token)
            transactions.extend(token_transactions)

        if transactions:
            await self.repository.update_last_transaction(transactions[0])

        return transactions

    async def _fetch_token_transactions(self, token: str, page: int = 1) -> list[dict[str, Any]]:
        """Loads transactions for a specific token, taking into account filtering."""
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
        """Gets a single page of transactions from the PolygonScan API."""
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
        async with session.get(PolygonScanScraper.BASE_URL, params=params, ssl=False) as response:
            print('Sending request...')
            return await response.json()

    async def _filter_new_transactions(self, transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filters only new transactions that have not yet been saved."""
        result = []
        for transaction in transactions:
            if await self._transaction_is_new(transaction):
                result.append(transaction)
            else:
                break

        return result

    async def _transaction_is_new(self, transaction: dict[str, Any]) -> bool:
        """Checks if the transaction is new compared to the last saved transaction."""
        last_transaction = await self.repository.get_last_transaction()
        return transaction.get('hash') != last_transaction.transaction_hash
