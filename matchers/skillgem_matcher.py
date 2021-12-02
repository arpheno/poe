from typing import List

from item import SkillGem


def match_skillgem(candidates:List[dict],item:SkillGem):
    conditions =[
        lambda x: x['gemLevel']==item.level,
        lambda x: x.get('corrupted',False)==item.corrupted,
        lambda x: x.get('gemQuality', 0) == item.quality,

    ]
    for candidate in candidates:
        if all(f(candidate) for f in conditions):
            return candidate
    if item.quality<20 or item.level <5:
        for candidate in candidates:
            if all(f(candidate) for f in conditions[:-1]):
                return candidate
    if item.quality==20:
        # this can return multiple versions of the gem i.e: lvl 1 and lvl 20
        # so we select the least valuable one
        return [ candidate for candidate in candidates if all(f(candidate) for f in conditions[1:])][-1]

    print(f"Couldn't find match for {item.name} {item.level} {item.quality} {'Corrupted' if item.corrupted else ''}",end=' ')
    approximate_match = candidates[-1]
    print(f"Using {item.name}, "
          f"{approximate_match.get('gemLevel',0)} "
          f"{approximate_match.get('gemQuality',0)} instead")
    return approximate_match