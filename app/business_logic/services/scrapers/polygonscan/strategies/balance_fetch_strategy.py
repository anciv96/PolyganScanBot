import aiohttp

from app.business_logic.services.scrapers.polygonscan.polygonscan_scraper import PolygonScanScraper
from app.config import POLYGON_SCAN_KEY
from app import logger_setup
from app.business_logic.repositories.transaction import TransactionRepository
from app.business_logic.services.scrapers.polygonscan.base_strategy import PolygonScanStrategy


logger = logger_setup.get_logger(__name__)


class AccountBalanceFetchStrategy(PolygonScanStrategy):

    async def fetch(self, token: str, repository: TransactionRepository) -> float:
        """
        Fetch balances for the provided tokens.

        Args:
            token (str): A list of token addresses to fetch transactions for.
            repository (TransactionRepository): A repository to manage transactions.

        Returns:
            List[dict[str, Any]]: A list of dictionaries containing the balance data.
        """
        self.token = token
        self.repository = repository

        balance = await self._get_balance(token)
        if balance.get('status') == '1':
            return float(balance.get('result'))

    async def _get_balance(self, address: str) -> dict:
        try:
            params = {
                "module": "account",
                "action": "balance",
                "address": address,
                "apikey": POLYGON_SCAN_KEY,
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(PolygonScanScraper.BASE_URL, params=params, ssl=False) as response:
                    result = await response.json()
                    return result
        except Exception as error:
            logger.error(error)
