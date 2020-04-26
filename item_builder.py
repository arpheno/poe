from ninja import retrieve_currency_rates
from stash_tabs import get_currency_tab

# excluded = ["Portal Scroll", "Scroll of Wisdom", "Exalted Orb", "Chaos Orb", "Orb of Transmutation",'Exalted Shard',"Stacked Deck"]
excluded=[]
def is_excluded(item):
    conditions=[]
    conditions.append(item.type_line in excluded)
    conditions.append(len(item.sockets)>4)

    if any(conditions):
        return True
    return False
def build_items():
    rates = retrieve_currency_rates()
    items = get_currency_tab()
    for item in [item for item in items if not is_excluded(item)]:
        item.price,item.type = rates.get(item.type_line, rates.get(item.name,(None, None)))
        if item.price:
            if item.stackSize<2:
                item.price=int(item.price)

    return items
if __name__ == '__main__':
    build_items()