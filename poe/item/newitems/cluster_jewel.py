from poe.item.newitems.base_item_model import Item


class ClusterJewel(Item):
    @property
    def significant_enchant(self):
        return (
            self.enchantMods[-1]
            .replace("Added Small Passive Skills grant: ", "")
            .replace("\n", ", ")
        )

    @property
    def hash_key(self):
        return {
            "ilvl": self.ilvl,
            "passives": self.enchantMods[0].split()[1],
            "significant_enchant": self.significant_enchant,
        }

