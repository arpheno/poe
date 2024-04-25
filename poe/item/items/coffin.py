from poe.item.items.item import Item


class Coffin(Item):
    @property
    def level(self):
        level = self.extract_property("Corpse Level")["values"][0][0].strip("%+()Max")
        return int(level)

    @property
    def quality(self):
        try:
            level = self.extract_property("Quality")["values"][0][0].strip("%+()Max")
            return int(level)
        except:
            return 0

    def match(self, prices: dict):
        if self.implicitMods:
            mods = self.implicitMods[0]
        else:
            return None
        candidates = (
        prices.get(mods)
        )
        if not candidates:
            return None
        candidates = filter(lambda x: x['levelRequired']<self.level, candidates )
        result = max(candidates, key=lambda x: x['levelRequired']) if candidates else None
        if result:
            self.typeLine=mods
            return result
        return None