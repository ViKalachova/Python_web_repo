import aiohttp
import asyncio
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from aiofile import async_open
from aiopath import AsyncPath
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)


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

async def get_exchange(qty=None):
    try:
        if qty is None:
            day = datetime.now().date()
            day_str = day.strftime('%d.%m.%Y')
            result = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={day_str}')
            return str(result)
        else:
            if int(qty) > 10:
                print("Please try to enter less than 10")
            result = []
            for i in range(int(qty)):
                day = datetime.now().date() - timedelta(i)
                day_str = day.strftime('%d.%m.%Y')
                resp = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={day_str}')
                result.append({day_str: resp})
            return str(result)
    except HttpError as err:
        print(err)


async def write_to_file(info):
    apath = AsyncPath("use_exchange_info.txt")
    if not await apath.exists():
        await apath.touch()
    async with async_open(apath, 'a') as afp:
        await afp.write(info)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message == 'exchange':
                exchange = await get_exchange()
                await self.send_to_clients(exchange)
                time_to_log = datetime.now()
                day_str = time_to_log.strftime('%d.%m.%Y %H:%M:%S')
                await write_to_file(f'{day_str} - {message} - {exchange}\n')
            elif len(message) > 8 and 'exchange' in message:
                exchange = await get_exchange(message[9])
                await self.send_to_clients(exchange)
                time_to_log = datetime.now()
                day_str = time_to_log.strftime('%d.%m.%Y %H:%M:%S')
                await write_to_file(f'{day_str} - {message} - {exchange}\n')
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())