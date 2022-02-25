from poe.item.items.item import Item


class ClusterJewel(Item):
    @property
    def level(self):
        level = self.extract_property("Level")["values"][0][0].strip("%+()Max")
        return int(level)

    @property
    def quality(self):
        try:
            level = self.extract_property("Quality")["values"][0][0].strip("%+()Max")
            return int(level)
        except:
            return 0


    def match(self, prices: dict):
        # significant_enchant= self.enchantMods[-1].split(':')[-1].strip()
        if not self.enchantMods:
            return
        significant_enchant = self.enchantMods[-1].replace("Added Small Passive Skills grant: ", "").replace("\n", ", ")
        candidates = prices.get(significant_enchant)
        conditions = [
            lambda x: x["levelRequired"] == self.ilvl,
            lambda x: x["variant"].split()[0] == self.enchantMods[0].split()[1],
            lambda x: x.get("gemQuality", 0) == self.quality,
        ]
        for candidate in candidates:
            if all(f(candidate) for f in conditions):
                return candidate

        return
