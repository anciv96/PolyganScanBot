from abc import ABC, abstractmethod

from app.business_logic.repositories.transaction import TransactionRepository


class PolygonScanStrategy(ABC):
    @abstractmethod
    async def fetch(self, token: str, repository: TransactionRepository):
        """
        Fetch data from PolygonScan using the provided strategy.

        Args:
            token (str): A token address to fetch data for.
            repository (TransactionRepository): A repository to manage transactions.

        Returns:
            List[dict[str, Any]]: A list of dictionaries containing the fetched data.
        """
        pass
