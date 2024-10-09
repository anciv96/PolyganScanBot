import asyncio
from typing import Any

import aiohttp

from app.config import POLYGON_SCAN_KEY
from app import logger_setup
from app.business_logic.repositories.transaction import TransactionRepository
from app.business_logic.services.scrapers.polygonscan.polygonscan_scraper import PolygonScanScraper
from app.business_logic.services.scrapers.polygonscan.base_strategy import PolygonScanStrategy


logger = logger_setup.get_logger(__name__)


class TransactionFetchStrategy(PolygonScanStrategy):

    async def fetch(self, token: str, repository: TransactionRepository) -> list[dict[str, Any]]:
        """
        Fetch transactions for the provided token.

        Args:
            token (List[str]): A token address to fetch transactions for.
            repository (TransactionRepository): A repository to manage transactions.

        Returns:
            List[dict[str, Any]]: A list of dictionaries containing the transaction data.
        """
        self.token = token
        self.repository = repository

        all_transactions = await self._fetch_all_transactions()
        return all_transactions

    async def _fetch_all_transactions(self) -> list[dict[str, Any]]:
        """Recursively loads all token transactions"""
        try:
            transactions = []
            token_transactions = await self._fetch_token_transactions(self.token)
            transactions.extend(token_transactions)

            if transactions:
                await self.repository.update_last_transaction(self.token, transactions[0])

            return transactions
        except Exception as error:
            logger.error(error)
            return []

    async def _fetch_token_transactions(self, token: str, page: int = 1) -> list[dict[str, Any]]:
        """Loads transactions for a specific token, taking into account filtering."""
        try:
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
        except Exception as error:
            logger.error(error)

    async def _fetch_transactions_page(self, session: aiohttp.ClientSession, token: str, page: int) -> dict[str, Any]:
        """Gets a single page of transactions from the PolygonScan API."""
        params = {
            "module": "account",
            "action": "txlist",
            "address": token,
            "startblock": 0,
            "endblock": 99999999,
            "page": page,
            "offset": 20,
            "sort": "desc",
            "apikey": POLYGON_SCAN_KEY,
        }
        try:
            async with session.get(PolygonScanScraper.BASE_URL, params=params, ssl=False) as response:
                logger.info(f'Sending transaction request ({token})...')
                await asyncio.sleep(1)
                return await response.json()
        except Exception as error:
            logger.error(error)

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
        try:
            last_transaction = await self.repository.get_last_transaction(self.token)
            return transaction.get('hash') != last_transaction.transaction_hash
        except Exception as error:
            logger.error(error)
