from async_lru import alru_cache

from app import logger_setup
from app.business_logic.models.database import async_session
from app.business_logic.repositories.transaction import TransactionRepository
from app.business_logic.services.files_manager.our_addresses_reader import get_our_tokens
from app.business_logic.services.scrapers.polygonscan.polygonscan_scraper import PolygonScanScraper
from app.business_logic.services.scrapers.polygonscan.strategies.balance_fetch_strategy import \
    AccountBalanceFetchStrategy


logger = logger_setup.get_logger(__name__)


async def create_message_text(transaction: dict[str, str], token):
    """
    Creates message text to send to admins in format:
        [WALLET]
        Name: Unknown wallet (0x802b...328b)
        [TRANSACTION]
        Type: Deposit
        Amount: 1,906.46 FAR
        [BALANCE CHANGE]
        214,053.03 FAR  215,959.49 FAR
        Link: https://polygonscan.com/tx/транзакция

    Parameters:
        transaction (dict): Transaction data.
        token (str): Token address.

    Returns:
        str: Text of the message.
    """
    transaction_type = await _get_transaction_type(transaction, token)

    wallet = transaction.get('from') if transaction_type == 'Deposit' else transaction.get('to')
    wallet_short = f"{wallet[:6]}...{wallet[-4:]}"
    wallet_name = await _get_wallet_name(wallet)
    amount = float(transaction['value']) / (10 ** 18)

    if amount != 0:
        _get_balance.cache_clear()

    balance = await _get_balance(token)
    to_balance = balance / (10 ** 18)
    from_balance = to_balance - amount if transaction_type == 'Deposit' else to_balance + amount
    link = f"https://polygonscan.com/tx/{transaction['hash']}"

    # Форматируем сообщение
    message = (
        f"<b>[WALLET]</b>\n"
        f"Name: {wallet_name} ({wallet_short})\n\n"
        f"<b>[TRANSACTION]</b>\n"
        f"Type: {transaction_type}\n"
        f"Amount: {amount:.4f} FAR\n\n"
        f"<b>[BALANCE CHANGE]</b>\n"
        f"{from_balance:.2f} FAR  ➝  {to_balance:.2f} FAR\n"
        f"Link: {link}"
    )
    return message


async def _get_transaction_type(transaction, token) -> str:
    if transaction['to'].lower() == token.lower():
        transaction_type = 'Deposit'
    elif transaction['from'].lower() == token.lower():
        transaction_type = 'Withdrawal'
    else:
        transaction_type = 'Transfer'

    return transaction_type


async def _get_wallet_name(address: str) -> str:
    all_our_tokens = await get_our_tokens()

    if our_token := all_our_tokens.get(address.lower()):
        name = our_token
    else:
        name = 'Unknown wallet'

    return name


async def _get_balance_scraper(token) -> PolygonScanScraper:
    async with async_session() as session:
        strategy = AccountBalanceFetchStrategy()
        repository = TransactionRepository(session)
        scraper = PolygonScanScraper(token, repository, strategy)

        return scraper





@alru_cache(32)
async def _get_balance(token):
    logger.info(f'Sending balance request ({token})...')
    balance_scraper = await _get_balance_scraper(token)
    balance = await balance_scraper.execute()

    return float(balance)

