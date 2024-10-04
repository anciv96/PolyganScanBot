# Абстрактный класс для PolygonScan с шаблонным методом
class PolygonScanScraper(Scraper):
    BASE_URL = 'https://api.polygonscan.com/api'

    def __init__(self, tokens: List[str], repository: TransactionRepository, strategy: PolygonScanStrategy):
        self.tokens = tokens
        self.repository = repository
        self.strategy = strategy

    async def execute(self) -> List[dict[str, Any]]:
        """Выполнить стратегию, заданную для PolygonScan."""
        return await self.strategy.fetch(self.tokens, self.repository)
