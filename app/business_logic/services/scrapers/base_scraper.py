from abc import abstractmethod, ABC
from typing import Any


class Scraper(ABC):
    @abstractmethod
    async def execute(self) -> list[dict[str, Any]]:
        """
        Execute the main logic of the scraper.

        This method should be implemented by subclasses to define how the scraping process is performed.

        Returns:
            List[dict[str, Any]]: A list of dictionaries containing the scraped data.
        """
        pass

