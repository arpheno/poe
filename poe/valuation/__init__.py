from poe.div_cards import div_card_values
from poe.scarabs.main import scarab_orb_of_horizon


def own_valuations():
    scarabs = scarab_orb_of_horizon()
    scarabs=scarabs[['price','value']].max(axis=1).reset_index()
    scarabs['name']=scarabs.tier+ ' ' + scarabs.kind + ' Scarab'
    scarabs=scarabs[['name',0]].set_index('name')[0].to_dict()
    div_cards = div_card_values()
    values={**scarabs,**div_cards}
    return values
if __name__ == '__main__':
    own_valuations()