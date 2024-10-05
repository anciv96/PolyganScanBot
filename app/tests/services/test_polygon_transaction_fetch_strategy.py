from unittest.mock import patch, AsyncMock

import pytest

from app.repositories.transaction import TransactionRepository
from app.services.scrapers.polygonscan.strategies.transaction_fetch_strategy import TransactionFetchStrategy


@pytest.mark.asyncio
async def test_fetch():
    tokens = ["0x123", "0x456"]
    mock_repository = AsyncMock(spec=TransactionRepository)
    strategy = TransactionFetchStrategy()

    strategy._fetch_all_transactions = AsyncMock(return_value=[{"hash": "abc123"}, {"hash": "def456"}])

    result = await strategy.fetch(tokens, mock_repository)

    assert len(result) == 2
    assert result[0]["hash"] == "abc123"
    assert strategy.tokens == tokens
    assert strategy.repository == mock_repository


@pytest.mark.asyncio
async def test_fetch_token_transactions():
    token = "0x123"
    page = 1
    strategy = TransactionFetchStrategy()

    mock_session = AsyncMock()

    strategy._fetch_transactions_page = AsyncMock(return_value={"status": "1", "result": [{"hash": "abc123"},
                                                                                          {"hash": "test2"}]})
    strategy._filter_new_transactions = AsyncMock(return_value=[{"hash": "abc123"}])

    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await strategy._fetch_token_transactions(token, page)

        assert len(result) == 1
        assert result[0]["hash"] == "abc123"
        strategy._fetch_transactions_page.assert_called_once()
        strategy._filter_new_transactions.assert_called_once()
