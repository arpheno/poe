# WS client example

import asyncio
import json
from asyncio import sleep
from pprint import pprint
from typing import Sequence

import aiohttp
import websockets


headers = {
    'Origin': 'https://www.pathofexile.com',
    'Cookie':'POESESSID=c820a16fbdfbfc95461d2b65e1714063'
}
extra_headers = list(headers.items())
pprint(extra_headers)
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
async def track_search(hash:str):
    print(f"tracking {hash}")
    uri = f"wss://www.pathofexile.com/api/trade/live/Metamorph/{hash}"
    async with aiohttp.ClientSession(headers=headers) as session:
        websocket_opts=dict(
            uri=uri,
            ssl=True,
            extra_headers=extra_headers,
            close_timeout=100,
            ping_interval=100000,
            ping_timeout=1000000
        )
        async with websockets.connect( **websocket_opts ) as websocket:
            while True:
                greeting = await websocket.recv()
                if "auth" in greeting:
                    continue
                for result in json.loads(greeting)["new"]:
                    html = await fetch(session, f"https://www.pathofexile.com/api/trade/fetch/{result}")
                    data = json.loads(html)['result'][0]
                    price =data['listing']['price']
                    seller =data['listing']['account']['lastCharacterName']
                    mods = data['item']['explicitMods']
                print(f'{hash} {mods} for {price} by {seller}')


async def track_all(*hashes):
    searches=[]
    for hash in hashes:
        searches.append(asyncio.create_task(track_search(hash)) )
        await sleep(1)
    for search in searches:
        await search
