import inspect

from poe.div_cards import rules
from poe.ninja import retrieve_prices

functions_list = inspect.getmembers(rules, inspect.isfunction)


def main():
    prices = retrieve_prices(
        [
            "SkillGem",
            "DivinationCard",
            "Fragment",
            "Currency",
            "Essence",
            "Fossil",
            "UniqueJewel",
            "Scarab",
            "Vial",
            "DeliriumOrb",
        ]
    )
    for name, func in functions_list[:-1]:
        print(f"{name}:{func(prices)}")

    pass


if __name__ == "__main__":
    main()
