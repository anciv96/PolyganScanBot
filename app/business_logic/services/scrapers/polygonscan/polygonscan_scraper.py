from app.business_logic.repositories.transaction import TransactionRepository
from app.business_logic.services.scrapers.base_scraper import Scraper
from app.business_logic.services.scrapers.polygonscan.base_strategy import PolygonScanStrategy


class PolygonScanScraper(Scraper):
    BASE_URL = 'https://api.polygonscan.com/api'

    def __init__(self, token: str, repository: TransactionRepository, strategy: PolygonScanStrategy):
        self.token = token
        self.repository = repository
        self.strategy = strategy

    async def execute(self):
        """
        Execute the strategy defined for PolygonScan.

        Returns:
            List[dict[str, Any]]: A list of dictionaries containing the scraped data.
        """
        return await self.strategy.fetch(self.token, self.repository)
