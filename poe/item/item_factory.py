from poe.item.base import Base
from poe.item.item import Item
from poe.item.map import Map
from poe.item.skill_gem import SkillGem

cls = {"map": Map, "skillgem": SkillGem, "base": Base}


def item_factory(type="item", **kwargs):
    return cls.get(type.lower(), Item)(type=type, **kwargs)