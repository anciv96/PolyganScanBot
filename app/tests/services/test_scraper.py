from unittest.mock import Mock, patch

import pytest

from app.config import TOKENS
from app.services.scraper import PolygonScanScraper


# @pytest.mark.asyncio
# async def test_get_transactions():
#     mock_repo = Mock()
#
#     polygon_scraper = PolygonScanScraper(TOKENS, mock_repo)
#
#     transactions = await polygon_scraper.get_transactions()
#
#     assert isinstance(transactions, list)
#
#     if transactions:
#         transaction = transactions[0]
#         isinstance(transaction, dict)
#         assert 'blockNumber' in transaction
#
@pytest.mark.asyncio
async def test_fetch_transactions():
    tokens = ["0xTokenAddress1", "0xTokenAddress2"]
    expected_transactions = [
        {
            "blockNumber": "19087857",
            "timeStamp": "1631600445",
            "hash": "0x72d4375b21207307ae0154542f1f9f3b99275596b846337efd30e6597e764f78"
        },
        {
            "blockNumber": "19089338",
            "timeStamp": "1631603783",
            "hash": "0xd70e432c764ed87eb8aa24c2741ca10b408a9232fdc0f4627e98a74fbc126feb"
        }
    ]
    scraper = PolygonScanScraper(tokens, None)

    with patch('aiohttp.ClientSession') as MockClientSession:
        mock_response = MockClientSession()
        mock_response.json.return_value = {
            "status": "1",
            "message": "OK",
            "result": expected_transactions,
        }
        MockClientSession.return_value.__aenter__.return_value.get.return_value = mock_response

        transactions = []
        async for transaction in scraper._fetch_transactions(tokens):
            transactions.append(transaction)

    assert transactions == expected_transactions





















