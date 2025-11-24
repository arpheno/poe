from collections import defaultdict

from poe.constants import LEAGUE
from poe.trade.stash_tabs.stash_tab_api import StashTabAPI


def add_tab_to_type_group(tab_data, groupings):
    groupings[tab_data['type']].add(tab_data['i'])
    groupings[tab_data['type'].lower()].add(tab_data['i'])


def add_tab_to_name_group(tab_data, groupings):
    groupings[tab_data['n']].add(tab_data['i'])
    groupings[tab_data['n'].lower()].add(tab_data['i'])


def add_tab_to_all_group(tab_data, groupings):
    groupings['all'].add(tab_data['i'])

def add_tab_to_special_group(tab_data, groupings):
    if  tab_data['type'] not in ['PremiumStash','QuadStash','NormalStash']:
        groupings['special'].add(tab_data['i'])


def add_tab_to_priced_group(tab_data: dict, groupings: dict):
    if '~price' in tab_data['n']:
        groupings['priced'].add(tab_data['i'])

default_rules=[
    add_tab_to_type_group,
    add_tab_to_name_group,
    add_tab_to_all_group,
    add_tab_to_priced_group,
    add_tab_to_special_group
]

class TabMapper:
    def __init__(self, grouping_rules: list[callable]=[]):
        self.groupings = defaultdict(set)
        self.tabs = {}
        self.grouping_rules = grouping_rules

    def add(self, tab_data):
        self.tabs[tab_data['i']] = tab_data
        for rule in self.grouping_rules+default_rules:
            rule(tab_data, self.groupings)
        return self.groupings

    def __getitem__(self, item):
        return self.groupings[item]

    def __repr__(self):
        return f"TabMapper({self.groupings})"

    def __str__(self):
        return str(self.groupings)


def retrieve_tab_mapping(mapper,stash_tab_api=StashTabAPI('swozn', LEAGUE, base_url="http://localhost:8999")):
    raw_data = stash_tab_api.fetch_tab_data(10)['tabs']
    for tab_data in raw_data:
        mapper.add(tab_data)
    return mapper

def main():
    mapper = TabMapper()
    tabs = retrieve_tab_mapping(mapper)
    # I want to sell only the special tabs, but not the currency tab
    selected_tabs = tabs['priced']|tabs['currencystash']

    print(selected_tabs)


if __name__ == '__main__':

    main()