from poe.item.base import Base
from poe.item.cluster_jewel import ClusterJewel
from poe.item.item import Item
from poe.item.map import Map
from poe.item.skill_gem import SkillGem

cls = {"map": Map, "skillgem": SkillGem, "base": Base,'clusterjewel':ClusterJewel}


def item_factory(type="item", **kwargs):
    return cls.get(type.lower(), Item)(type=type, **kwargs)