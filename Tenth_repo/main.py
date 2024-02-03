import platform
import sys

import aiohttp
import asyncio
from datetime import datetime, timedelta
from time import time


class HttpError(Exception):
    pass


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    value = {}
                    for el in result['exchangeRate']:
                        if el['currency'] == 'EUR':
                            value['EUR'] = {'sale': el['saleRate'], 'purchase': el['purchaseRate']}
                        elif el['currency'] == 'USD':
                            value['USD'] = {'sale': el['saleRate'], 'purchase': el['purchaseRate']}
                    return value
                else:
                    raise HttpError(f"Error status: {response.status} for {url}")
        except (aiohttp.ClientConnectionError, aiohttp.InvalidURL) as err:
            raise HttpError(f"Error status: {response.status} for {url}")


async def main(qty):
    start = time()
    if int(qty) > 10:
        print("Please try to enter less than 10")
    try:
        result = []
        for i in range(int(qty)):
            day = datetime.now().date() - timedelta(i)
            day_str = day.strftime('%d.%m.%Y')
            resp = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={day_str}')
            result.append({day_str:resp})
        finish = time() - start
        print(finish)
        return result
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(sys.argv[1]))
    print(r)
