from poe.item.newitems.base_item_model import Item


class Map(Item):
    @property
    def map_tier(self):
        map_tier = self.extract_property("Map Tier").values[0][0]
        return int(map_tier)

    @property
    def hash_key(self):
        return [{'name': self.typeLine, 'tier': self.map_tier}]
