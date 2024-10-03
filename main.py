import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.polygonscan.com/api?"
                f"module=account"
                f"&action=txlist"
                f"&startblock=0"
                f"&endblock=99999999"
                f"&offset=10"
                f"&sort=desc"
                f"&address=0x5f32abeebd3c2fac1e7459a27e1ae9f1c16cccca"
                f"&apikey=6Z9J4RRTSRPZF9ZDAMGQPRWNEYMWA25NEI",
                ssl=False) as response:
            resp = await response.json()
            for key, value in resp['result'][0].items():
                print(key, value)
                print()
                print()


if __name__ == '__main__':
    asyncio.run(main())
