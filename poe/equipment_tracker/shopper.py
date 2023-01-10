from poe.equipment_tracker.direct_whisperer import DirectWhisperer
from poe.equipment_tracker.tracker import Tracker

async def make_shopper(hash):
    direct_whisperer = DirectWhisperer()
    tracker = Tracker(hash)
    async for result in tracker.results():
        print(f"whispering {hash}")
        direct_whisperer.direct_whisper(result['listing']['whisper_token'])


async def main(hashes):
    shoppers = [make_shopper(trade_hash) for trade_hash in hashes]
    await asyncio.gather(*shoppers)


import asyncio

if __name__ == "__main__":
    artist35 = '0VyB6q7cg'
    enlightened_65 = 'YaK8llgSY'
    everchanging_2 = 'r7VwJBRiQ'
    temples = "PyBGnJ7UL"
    sick_shield = 'RkPJ7gOH7'
    dragons_heart_130 = '8WaBavnSV'
    abyssal_orb = 'vywere9SE'
    secondary_regrading_lens1_1 = 'ZrPlgg6fQ'
    secondary_regrading_lens275 = 'GOvk0OZFb'
    doryanis_epiphany_110 = 'd7zywaRiJ'
    home_55 = '9rWbmPQfK'
    gemcutters_mercy_50 = 'MOQzbdqFJ'
    gemcutters_mercy_55 = '39EJ5L0i5'
    w_a_p_1_div = 'Zr668aYfQ'
    hashes = [home_55,gemcutters_mercy_55]#,secondary_regrading_lens1_1,secondary_regrading_lens275]
    asyncio.get_event_loop().run_until_complete(main(hashes))
