from poe.bulk.report_processing.amount_fixer import fix_amount



def match_names(name):
    if any(x in name for x in ['gilded','rusted','polished','winged']):
        return f'{name.lower()} scarab'
    return name
