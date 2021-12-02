from typing import List

from constants import blacklist
from item import Item
from matchers.base_matcher import match_base
from matchers.map_matcher import match_map
from matchers.skillgem_matcher import match_skillgem
from ninja import retrieve_currency_rates
from stash_tabs import get_all_tabs

excluded=[]
def is_excluded(item):
    conditions=[]
    conditions.append(item.type_line in blacklist)
    conditions.append(item.name in blacklist)
    conditions.append(len(item.sockets)>4)

    if any(conditions):
        return True
    return False

def type_mapping(rates):
    all_rates={key:values for m in rates.maps for key,values in m.items()}
    return {name:first['type'] for name,(first,*_ ) in all_rates.items()}


def build_items():
    rates = retrieve_currency_rates()
    mapping = type_mapping(rates)
    items = get_all_tabs(mapping)
    items=[item for item in items if not is_excluded(item)]
    _build_items(items, rates)
    return [item for item in items if not item.stashtab == 'noindex']



def _build_items(items:List[Item], rates):
    for item in items:
        if item.name == 'Chaos Orb':
            item.price = 1
            continue

        candidates = rates.get(item.name) or rates.get(item.typeLine) or rates.get(item.baseType)
        if item.type == 'SkillGem':
            exact_match = match_skillgem(candidates, item)
        elif item.type == 'BaseType' or item.type=='Base':
            if 'jewel' in item.name.lower():
                exact_match=None
            else:
                exact_match = match_base(candidates, item)
        elif item.type == 'Map':
            exact_match = match_map(
                candidates, item
            )
        else:
            exact_match = candidates[0]
        item.price = exact_match and exact_match['chaosValue']


if __name__ == '__main__':
    build_items()