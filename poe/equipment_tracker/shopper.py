
from asyncio import sleep

import requests

from poe.equipment_tracker.tracker import Tracker
from poe.trade.headers import headers


def direct_whisper(token):
    url = 'https://www.pathofexile.com/api/trade/whisper'
    response = requests.post(url, json=dict(token=token), headers={'x-requested-with': 'XMLHttpRequest', **headers})
    return response.json()


def whisper_seller(data):
    direct_whisper(data['listing']['whisper_token'])


async def make_shopper(hash):
    behaviour = whisper_seller
    tracker = Tracker(hash)
    async for result in tracker.results():
        behaviour(result)



async def main(hashes):
    shoppers= [make_shopper(trade_hash) for trade_hash in hashes]
    await asyncio.gather(*shoppers)



import asyncio

if __name__ == "__main__":
    hashes = ["Kjjo6pgC5"]
    asyncio.get_event_loop().run_until_complete(main(hashes))
