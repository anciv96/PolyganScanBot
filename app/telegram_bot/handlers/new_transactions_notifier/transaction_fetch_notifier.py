import asyncio

from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError, TelegramBadRequest

from app import logger_setup
from app.business_logic.models.database import async_session
from app.business_logic.repositories.transaction import TransactionRepository
from app.business_logic.services.scrapers.polygonscan.polygonscan_scraper import PolygonScanScraper
from app.business_logic.services.scrapers.polygonscan.strategies.transaction_fetch_strategy import \
    TransactionFetchStrategy
from app.config import TOKENS, ADMIN_IDS
from app.dispatcher import bot
from app.telegram_bot.handlers.new_transactions_notifier.message_text import create_message_text

logger = logger_setup.get_logger(__name__)


async def notify() -> None:
    """
      Notify users of new transactions for a list of tokens.

      This function iterates through a list of tokens, retrieves transaction data using
      a transaction scraper, and sends a notification for each transaction in reverse order.
      A delay of 1 second is introduced between each message to avoid overwhelming the message service.

      Returns:
          None
      """
    for token in TOKENS:
        transaction_scraper = await _get_transaction_scraper(token)
        transactions = await transaction_scraper.execute()

        for transaction in transactions[::-1]:
            message_text = await create_message_text(transaction, token)
            await _send_message(message_text)
            await asyncio.sleep(1)


async def _get_transaction_scraper(token) -> PolygonScanScraper:
    async with async_session() as session:
        strategy = TransactionFetchStrategy()
        repository = TransactionRepository(session)
        scraper = PolygonScanScraper(token, repository, strategy)

        return scraper


async def _send_message(message: str):
    for admin in ADMIN_IDS:
        try:
            await bot.send_message(admin, message, disable_web_page_preview=True)
        except TelegramRetryAfter as error:
            logger.warning(error)
            await asyncio.sleep(20)
        except TelegramForbiddenError as error:
            logger.warning(error)
        except TelegramBadRequest as error:
            logger.warning(error)
