# WS client example

import asyncio
import json
from asyncio import sleep
from pprint import pprint

import aiohttp
import websockets

from poe.constants import ssid, LEAGUE

headers = {
    "Origin": "https://www.pathofexile.com",
    "Cookie": f"POESESSID={ssid}",
    "User-Agent": "Mozilla/5.011 Macintosh",
}

extra_headers = list(headers.items())
pprint(extra_headers)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def track_search(hash: str):
    print(f"tracking {hash}")
    uri = f"wss://www.pathofexile.com/api/trade/live/{LEAGUE}/{hash}"
    async with aiohttp.ClientSession(headers=headers) as session:
        websocket_opts = dict(
            uri=uri,
            ssl=True,
            extra_headers=extra_headers,
            close_timeout=10,
            ping_interval=10000,
            ping_timeout=10000,
        )
        async with websockets.connect(**websocket_opts) as websocket:
            while True:
                greeting = await websocket.recv()
                if "auth" in greeting:
                    continue
                for result in json.loads(greeting)["new"]:
                    html = await fetch(
                        session, f"https://www.pathofexile.com/api/trade/fetch/{result}"
                    )
                    data = json.loads(html)["result"][0]
                    return data
                    # price = data["listing"]["price"]
                    # seller = data["listing"]["account"]["lastCharacterName"]
                    # mods = data["item"]["explicitMods"]
                # print(f"{hash} {mods} for {price} by {seller}")


async def track_all(*hashes):
    searches = []
    for hash in hashes:
        searches.append(asyncio.create_task(track_search(hash)))
        await sleep(5)
    for search in searches:
        await search
