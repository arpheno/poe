def is_chaos_orb(item, type_mapping):
    return "Currency" if item["name"] == "Chaos Orb" else None


def is_item_exact_match(item, type_mapping):
    return type_mapping.get(item["name"]) or type_mapping.get(item["name"] + " Support")

def is_item_influenced(item, type_mapping):
    return 'Base' if item.get("influences") else None

def determine_type(item, type_mapping):
    determiners = [is_chaos_orb, is_item_exact_match,is_item_influenced]
    for f in determiners:
        if f(item, type_mapping):
            return f(item, type_mapping)
    else:
        return None
    try:
        return next(f(item, type_mapping) for f in determiners if f(item,type_mapping) is not None)
    except StopIteration:
        return None
