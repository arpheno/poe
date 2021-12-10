from typing import List

from poe.item.base import Base


def match_base(candidates:List[dict],item:Base):
    conditions =[
        lambda x: str(x.get('variant')).lower()==('/'.join(item.influences) or 'none'),
        lambda x: x['levelRequired']== item.ilvl,
    ]
    for candidate in candidates:
        if all(f(candidate) for f in conditions):
            return candidate
    return None
