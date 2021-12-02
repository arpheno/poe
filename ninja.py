from collections import ChainMap, defaultdict
from pprint import pprint

import pandas as pd

import requests


def retrieve_currency_rates():
    currs = ["Fragment", "Currency"]
    # currs = [ "Currency"]
    rates = [ask_ninja("https://poe.ninja/api/data/currencyoverview", curr,) for curr in currs]
    items = [
        "Scarab",
        "Oil",
        "Fossil",
        "Resonator",
        "Prophecy",
        "Incubator",
        "UniqueMap",
        "UniqueJewel",
        "UniqueFlask",
        "UniqueArmour",
        "UniqueWeapon",
        "UniqueAccessory",
        "Essence",
        "DeliriumOrb",
        "DivinationCard",
        "Map",
        "SkillGem",
        "BaseType"
    ]
    rates += [ask_ninja("https://poe.ninja/api/data/itemoverview", curr,) for curr in items]
    return ChainMap(*[rate for rate in rates])
key_builders = {''}


class DefaultBuilder:
    def __call__(self, item):
        pass


def key_builder_factory(type):
    return key_builders.get('type',DefaultBuilder())
def ask_ninja(url, type, league="Scourge"):
    params = dict(type=type, league=league)
    response = requests.get(url=url, params=params)
    print(url,type,response.status_code)
    data = response.json()
    for c in data['lines']:
        if type in ('Fragment','Currency') and not c.get('receive'):
            continue
        if not c.get('name'):
            c['name']=c['currencyTypeName']
            c['chaosValue']=c["receive"]["value"]
        c['type']=type
    return_value = defaultdict(list)
    for c in data['lines']:
        if type in ('Currency','Fragment') and not c.get('receive'):
            continue
        return_value[c['name']].append(c)
    return dict(return_value)
def lookup_key(item):
    return ()

def _currencyreport(url, type, league="Scourge"):
    params = dict(type=type, league=league)
    response = requests.get(url=url, params=params)
    print(url, type, response.status_code)
    data = response.json()
    lines = [line for line in data['lines'] if 'pay' in line if 'receive' in line]
    first = [pd.Series(c["receive"]) for c in lines]
    second = [pd.Series(c["pay"]) for c in lines]
    result = pd.concat(first+second, axis=1).T
    currency_details= pd.DataFrame(data['currencyDetails']).set_index('id')['name']
    result['pay_currency']=result['pay_currency_id'].map(currency_details)
    result['get_currency']=result['get_currency_id'].map(currency_details)
    return result

def currencyreport():
    currs = ["Fragment", "Currency"]
    # currs = ["Currency"]
    rates = pd.concat([_currencyreport("https://poe.ninja/api/data/currencyoverview", curr,) for curr in currs])
    return rates.dropna()
def refine_report(cr):
    cr['receive'] = (cr['pay_currency'] == 'Chaos Orb')
    cr['sample_time_utc'] = pd.to_datetime(cr['sample_time_utc'])
    cr['value'] = cr['value'].astype('float64')
    cr.loc[cr.pay_currency != 'Chaos Orb', 'value'] = 1 / cr.loc[cr.pay_currency != 'Chaos Orb', 'value']
    cr.loc[cr.pay_currency != 'Chaos Orb', 'get_currency'] = cr[cr.pay_currency != 'Chaos Orb']['pay_currency']
    cr.loc[cr.pay_currency != 'Chaos Orb', 'pay_currency'] = 'Chaos Orb'
    return cr

if __name__ == '__main__':
    a=currencyreport()
    ask_ninja("https://poe.ninja/api/data/currencyoverview", 'Currency'
                                                             , )
