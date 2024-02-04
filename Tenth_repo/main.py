import platform
import sys

import aiohttp
import asyncio
from datetime import datetime, timedelta
from time import time


class HttpError(Exception):
    pass


async def request(url, currency=None):
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
                        elif el['currency'] == currency:
                            try:
                                value[currency] = {'sale': el['saleRate'], 'purchase': el['purchaseRate']}
                            except KeyError:
                                value[currency] = {'saleNB': el['saleRateNB'], 'purchaseNB': el['purchaseRateNB']}
                    return value
                else:
                    raise HttpError(f"Error status: {response.status} for {url}")
        except (aiohttp.ClientConnectionError, aiohttp.InvalidURL) as err:
            raise HttpError(f"Error status: {response.status} for {url}")


async def main(arg):
    start = time()
    if int(arg[1]) > 10:
        print("Please try to enter less than 10")
    try:
        result = []
        for i in range(int(arg[1])):
            day = datetime.now().date() - timedelta(i)
            day_str = day.strftime('%d.%m.%Y')
            if len(arg) == 3:
                resp = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={day_str}', arg[2])
            else:
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
    r = asyncio.run(main(sys.argv))
    print(r)