from typing import Any

from app.repositories.transaction import TransactionRepository
from app.services.scrapers.base_scraper import Scraper
from app.services.scrapers.polygonscan.base_strategy import PolygonScanStrategy


class PolygonScanScraper(Scraper):
    BASE_URL = 'https://api.polygonscan.com/api'

    def __init__(self, tokens: list[str], repository: TransactionRepository, strategy: PolygonScanStrategy):
        self.tokens = tokens
        self.repository = repository
        self.strategy = strategy

    async def execute(self) -> list[dict[str, Any]]:
        """
        Execute the strategy defined for PolygonScan.

        Returns:
            List[dict[str, Any]]: A list of dictionaries containing the scraped data.
        """
        return await self.strategy.fetch(self.tokens, self.repository)
