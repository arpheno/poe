import inspect

from constants import blacklist, currency_shards
from poe.div_cards import rules
from poe.ninja import retrieve_prices

prices = retrieve_prices(["DivinationCard"])

rules_list = inspect.getmembers(rules, inspect.isfunction)

def main():
    valuable = {
        key: value
        for key, value in prices.items()
        if not key in blacklist
        if value[0]["chaosValue"] >1
        if not key in currency_shards
        if not key.lower().replace("'", "").replace(" ", "_") in [name for name,func in rules_list]
    }
    for key, value in valuable.items():
        mods=value[0]["explicitModifiers"][0]['text']
        stacksize = value[0].get("stackSize", 1)
        print(f'\n\n{key} : {value[0].get("chaosValue")} {stacksize} {mods}')
        if 'uniqueitem' in mods:
            item = mods[mods.find('{') + 1:]
            item = item[:item.find('}')]
            print(f'"{key}":((1/{stacksize}),"{item}"),')
    pass


if __name__ == "__main__":
    main()

a={

}