from poe.constants import blacklist
from poe.ninja import retrieve_prices
from poe.valuation.div_cards import rules
from poe.valuation.div_cards.generic import apply_fixed_rules
from poe.valuation.div_cards.rules import xxxmap_div_card_name, div_card_rules
import logging
import statistics
import pandas

logger = logging.getLogger(__name__)


def div_card_values(prices):
    rule_based = {}
    for name, func in div_card_rules.items():
        try:
            rule_based[name] = func(prices)
        except ValueError:
            pass
        except Exception:
            logger.exception(f"Can't value {name}")

    generic = {key: value for key, value in apply_fixed_rules(prices).items()}
    blacklisted = {key: 0 for key in blacklist}
    return {**rule_based, **generic, **blacklisted}

def bestprice(card, price):
    relevant = [
        item
        for items in prices.values()
        for item in items
        if str(card) in item["name"]
    ]
    values = [item["chaosValue"] for item in relevant]
    if values:
        value =  price / statistics.mean(values)
        return card, value
    else:
        return card, None


if __name__ == "__main__":
    prices = retrieve_prices()
    # with open("prices.json", "r") as f:
    #     prices = json.load(f)
    sorted_dict = sorted(div_card_values(prices).items(), key=lambda x:x[1])
    filtered_list = [item for item in sorted_dict if item[1] > 2]
    pprint.pprint(filtered_list)

    print()
    print()
    print()

    results = []
    for name, value in filtered_list:
        result = bestprice(name, value)
        results.append(result)
    best_prices = sorted(results, key=lambda x: x[1], reverse= True)
    pprint.pprint(best_prices)

    output_filename = "combined_results.txt"

    with open(output_filename, "w") as f:
        f.write("Card prices:\n")
        f.write("-----------------\n")
        for item in filtered_list:
            f.write(f"{item[0]}: {item[1]}\n")
        f.write("\n")

        f.write("Most lucrative card:\n")
        f.write("-----------------\n")
        for item in best_prices:
            f.write(f"{item[0]}: {item[1]}\n")

    print(f"Results written to {output_filename}")