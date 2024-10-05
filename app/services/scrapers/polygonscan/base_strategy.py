from abc import ABC, abstractmethod
from typing import Any

from app.repositories.transaction import TransactionRepository


class PolygonScanStrategy(ABC):
    @abstractmethod
    async def fetch(self, tokens: list[str], repository: TransactionRepository) -> list[dict[str, Any]]:
        """
        Fetch data from PolygonScan using the provided strategy.

        Args:
            tokens (List[str]): A list of token addresses to fetch data for.
            repository (TransactionRepository): A repository to manage transactions.

        Returns:
            List[dict[str, Any]]: A list of dictionaries containing the fetched data.
        """
        pass
