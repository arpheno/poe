from poe.item.item import Item


class Map(Item):
    @property
    def map_tier(self):
        map_tier = self.extract_property('Map Tier')['values'][0][0]
        return int(map_tier)