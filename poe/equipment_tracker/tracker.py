import json

import aiohttp
import websockets

from constants import LEAGUE, ssid

headers = {
    "Origin": "https://www.pathofexile.com",
    "Cookie": f"POESESSID={ssid}",
    "User-Agent": "Mozilla/5.011 Macintosh",
}


class Tracker:
    def __init__(self, hash: str):
        self.hash = hash
        self.websocket_opts = dict(
            ssl=True,
            extra_headers=list(headers.items()),
            close_timeout=10,
            ping_interval=10000,
            ping_timeout=10000,
        )
        self.session = None

    async def retrieve_listing(self, message):
        if self.session == None:
            self.session = aiohttp.ClientSession(headers=headers)
        for result in message:
            details_page = f"https://www.pathofexile.com/api/trade/fetch/{result}"
            async with self.session.get(details_page) as response:
                html = await response.text()
            data = json.loads(html)["result"][0]
            yield data

    async def results(self):
        async for message in self.retrieve_message(self.hash):
            async for result in self.retrieve_listing(message):
                yield result

    async def retrieve_message(self, hash: str):
        uri = f"wss://www.pathofexile.com/api/trade/live/{LEAGUE}/{hash}"
        print(f"tracking {hash}")
        async with websockets.connect(uri=uri, **self.websocket_opts) as websocket:
            while True:
                message = await websocket.recv()
                if "auth" in message:
                    continue
                else:
                    yield json.loads(message)["new"]
