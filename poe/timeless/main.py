import asyncio
from poe.timeless.seeds import seeds
from poe.timeless.timeless_hash import find_doryiani

from poe.timeless.tracker import track_all

if __name__ == '__main__':
    hashes=['8BjgOvIV']
    # for name_of, seeds in seeds.items():
    #     hashes += [find_doryiani(seed, name_of) for seed in seeds[:6]]
    #     print(hashes)
    print(hashes)
    asyncio.get_event_loop().run_until_complete(track_all(*hashes))
