from poe.ninja import retrieve_prices
import pandas as pd
gem_names={key:value for key,value in enumerate(['Anomalous','Divergent','Phantasmal','Superior'])}
gem_indexes={value:key for key,value in gem_names.items()}
def xp_value(prices):
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem
        for gem in gems
        if gem['sparkline']['data']
    #     if 'Enlighten' in gem['name']
        if gem['variant'] in('3','5/20','5','20','1')
    ]
    df=pd.DataFrame(relevant_gems)
    analysis=pd.DataFrame()
    analysis['profit']=df.groupby('name')['chaosValue'].max()-df.groupby('name')['chaosValue'].min()
    analysis['cost']=df.groupby('name')['chaosValue'].min()
    analysis['icon']=analysis.index.map(df.groupby('name')['icon'].min())
    analysis['relative_profit']=(df.groupby('name')['chaosValue'].max()-df.groupby('name')['chaosValue'].min())/df.groupby('name')['chaosValue'].min()
    analysis=analysis.sort_values('profit',ascending=False).reset_index()
    analysis['gem_type']=analysis['name'].apply(lambda x: 'special' if any(y in x  for y in ('Enhance Support','Enlighten Support','Empower Support')) else 'Awakened' if 'Awakened' in x else 'normal')
    exp_needed={}
    exp_needed['normal']=341_331_311.0
    exp_needed['special']=1_439_190_228+226_854_909
    exp_needed['Awakened']=411_225_217+452_347_738+497_582_512+547_340_764
    analysis['xp_needed'] = analysis.gem_type.map(exp_needed)
    analysis['profit_with_qual_bow'] = analysis.profit * analysis.gem_type.map(
        {'Awakened': 1, 'normal': 1, 'special': 1.65})
    analysis['xp_value'] = analysis.profit_with_qual_bow / analysis.xp_needed
    result= analysis.sort_values('xp_value', ascending=False)
    return result
if __name__ == '__main__':
    prices=retrieve_prices(['SkillGem'])
    temp=xp_value(prices)
    print(temp)