# Интерфейс для стратегий PolygonScan
class PolygonScanStrategy(ABC):
    @abstractmethod
    async def fetch(self, tokens: List[str], repository: TransactionRepository) -> List[dict[str, Any]]:
        """Метод для получения данных из PolygonScan."""
        pass
