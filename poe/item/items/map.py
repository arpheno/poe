from poe.item.items.item import Item


class Map(Item):
    @property
    def map_tier(self):
        map_tier = self.extract_property("Map Tier")["values"][0][0]
        return int(map_tier)

    def match(self, prices: dict):
        candidates = (
            prices.get(self.name)
            or prices.get(self.typeLine)
            or prices.get(self.baseType)
        )
        conditions = [
            lambda x: x["mapTier"] == self.map_tier,
        ]
        for candidate in candidates:
            if all(f(candidate) for f in conditions):
                return candidate
        print(f"Couldn't find match for {self.name} {self.map_tier}", end=" ")
        approximate_match = candidates[-1]
        print(f"Using {self.name}, " f"{approximate_match['mapTier']} ")
        return approximate_match
