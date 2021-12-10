from itertools import groupby
from pprint import pprint
import pandas as pd
from poe.ninja import retrieve_prices
def profit(df,key):
    temp = df.drop(key,axis=1)
    return temp.mean(axis=1)- df[key]*2
def profitability(df,key):
    temp = df.drop(key,axis=1)
    return (temp.mean(axis=1)- df[key]*2)/df[key]
def profit_analysis(df,key):
    analysis = pd.concat([profitability(df, key), profit(df, key)], axis=1,keys=['profitability','profit'])
    analysis['kind']=key
    return analysis


def scarab_orb_of_horizon():
    global values, analysis
    prices = retrieve_prices(['Scarab'])
    groups = groupby(sorted(prices.items()), key=lambda x: x[0].split()[0])
    values = {key: {x[0].split()[1]: x[1][0]['chaosValue'] for x in values} for key, values in groups}
    df = pd.DataFrame(values).T
    df = df.drop('Lure', axis=1)
    df = df.drop('Craicic').drop('Farric').drop('Fenumal').drop('Saqawine')
    df['mean'] = df.mean(axis=1)
    analysis = pd.concat([profit_analysis(df, key) for key in df.keys()]).reset_index()
    analysis.columns = ['tier', 'profitability', 'profit', 'kind']
    analysis = analysis.set_index(['tier', 'kind'])


if __name__ == '__main__':
    scarab_orb_of_horizon()
