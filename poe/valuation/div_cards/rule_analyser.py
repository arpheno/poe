from constants import blacklist
from poe.ninja import retrieve_prices
from poe.valuation.div_cards.fixed import currency_shards
from poe.valuation.div_cards.generic import rules_list


def analyse_rules():
    prices = retrieve_prices(["DivinationCard"])
    valuable = {
        key: value
        for key, value in prices.items()
        if not key in blacklist
        if value[0]["chaosValue"] > 1
        if not key in currency_shards
        if not key.lower().replace("'", "").replace(" ", "_") in [name for name, func in rules_list]
    }
    for key, value in valuable.items():
        try:
            mods = value[0]["explicitModifiers"][0]["text"]
        except Exception as e:
            print(f"{key} fucked up")
            continue
        stacksize = value[0].get("stackSize", 1)
        print(f'\n\n{key} : {value[0].get("chaosValue")} {stacksize} {mods}')
        if "uniqueitem" in mods:
            item = mods[mods.find("{") + 1 :]
            item = item[: item.find("}")]
            print(f'"{key}":((1/{stacksize}),"{item}"),')