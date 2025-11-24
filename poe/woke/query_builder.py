from poe.woke.mod_mapper import Mod


class Query:
    pass


def add_mods(query: dict, mods: dict):
    filters = [
        {
            'id': mod.id,
            'value': {'min': mod.value},
        }
        for mod in mods
    ]
    query['query']['stats'][0]['filters'] = filters
    return query


def add_type(query: dict, item_type: str):
    query['query']['type'] = item_type
    return query


def add_misc(query: dict, misc: dict):
    query['query']['filters']['misc_filters'] = misc
    return query


registry = {
    'mods': add_mods,
    'type': add_type,
    'misc': add_misc,
}


def build_query(**kwargs):
    query = {
        'query': {
            'status': {'option': 'online'},
            'filters': {},
            'stats': [
                {'type': 'and', 'filters': []}
            ]
        }
    }
    for func_type, args in kwargs.items():
        query = registry[func_type](query, args)

    return query
