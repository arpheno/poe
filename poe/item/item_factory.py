from poe.item.items.basetype import BaseType
from poe.item.items.cluster_jewel import ClusterJewel
from poe.item.items.item import Item
from poe.item.items.map import Map
from poe.item.items.skill_gem import SkillGem

cls = {
    "map": Map,
    "skillgem": SkillGem,
    "basetype": BaseType,
    "clusterjewel": ClusterJewel,
}


def item_factory(type="item", **kwargs):
    return cls.get(type.lower(), Item)(type=type, **kwargs)
