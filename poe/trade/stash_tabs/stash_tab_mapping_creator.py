from collections import defaultdict

from trade.stash_tabs.caller import stash_tab_api_interactor


class FlexiDict:
    def __init__(self, elements=None):
        if elements is None:
            self.elements = {}
        else:
            self.elements = dict(elements)

    def __add__(self, other):
        """Merge two dictionaries. In case of key conflict, other's value takes precedence."""
        new_dict = FlexiDict(self.elements)
        if isinstance(other, FlexiDict):
            new_dict.elements.update(other.elements)
        elif isinstance(other, dict):
            new_dict.elements.update(other)
        return new_dict

    def __sub__(self, other):
        """Remove keys found in 'other' from this dictionary."""
        new_dict = FlexiDict(self.elements)
        if isinstance(other, FlexiDict):
            keys_to_remove = other.elements.keys()
        elif isinstance(other, dict):
            keys_to_remove = other.keys()
        else:
            raise ValueError("Subtraction requires a FlexiDict or dict type.")
        for key in keys_to_remove:
            new_dict.elements.pop(key, None)
        return new_dict

    def __repr__(self):
        return f"FlexiDict({self.elements})"


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


def retrieve_tab_mapping(mapper):
    raw_data = stash_tab_api_interactor(10)['tabs']
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