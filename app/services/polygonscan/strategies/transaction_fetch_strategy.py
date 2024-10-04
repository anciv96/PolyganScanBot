s


# Стратегия получения транзакций
class TransactionFetchStrategy(PolygonScanStrategy):
    async def fetch(self, tokens: List[str], repository: TransactionRepository) -> List[dict[str, Any]]:
        """Получить транзакции для заданных токенов."""
        transactions = []
        async with aiohttp.ClientSession() as session:
            for token in tokens:
                page = 1
                while True:
                    params = {
                        "module": "account",
                        "action": "txlist",
                        "address": token,
                        "startblock": 0,
                        "endblock": 99999999,
                        "page": page,
                        "offset": 10,
                        "sort": "desc",
                        "apikey": POLYGON_SCAN_KEY,
                    }
                    async with session.get(PolygonScanScraper.BASE_URL, params=params, ssl=False) as response:
                        data = await response.json()
                        fetched_transactions = data.get("result", [])

                        if data.get("status") != "1" or not fetched_transactions:
                            break

                        new_transactions = await self._filter_new_transactions(repository, fetched_transactions)
                        transactions.extend(new_transactions)

                        if len(new_transactions) < len(fetched_transactions):
                            break

                        page += 1

        if transactions:
            await repository.update_last_transaction(transactions[0])

        return transactions