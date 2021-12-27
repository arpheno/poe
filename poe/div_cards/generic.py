import inspect

from constants import blacklist, currency_shards
from poe.div_cards import rules
from poe.ninja import retrieve_prices


rules_list = inspect.getmembers(rules, inspect.isfunction)

def analyse_rules():
    prices = retrieve_prices(["DivinationCard"])
    valuable = {
        key: value
        for key, value in prices.items()
        if not key in blacklist
        if value[0]["chaosValue"] >1
        if not key in currency_shards
        if not key.lower().replace("'", "").replace(" ", "_") in [name for name,func in rules_list]
    }
    for key, value in valuable.items():
        try:
            mods=value[0]["explicitModifiers"][0]['text']
        except Exception as e:
            print(f'{key} fucked up')
            continue
        stacksize = value[0].get("stackSize", 1)
        print(f'\n\n{key} : {value[0].get("chaosValue")} {stacksize} {mods}')
        if 'uniqueitem' in mods:
            item = mods[mods.find('{') + 1:]
            item = item[:item.find('}')]
            print(f'"{key}":((1/{stacksize}),"{item}"),')
    pass
def expand_currency_shards(prices):
    result={}
    for splinter,(fraction,reward) in currency_shards.items():
        reward_price=min([price for price in prices.get(reward,[{}])],key=lambda x: x.get('links',0))
        if reward_price:
            result[splinter]=fraction*reward_price["chaosValue"]
        else:
            result[splinter]=0
    return result

if __name__ == "__main__":
    prices=retrieve_prices()
    result=expand_currency_shards(prices)
    for key,value in result.items():
        reward_price = min([price for price in prices.get(key, [{}])], key=lambda x: x.get('links', 0))
        if reward_price:
            print(f'{key} ninja {reward_price["chaosValue"]} own {value} diff {reward_price["chaosValue"]-value}')
    # analyse_rules()
