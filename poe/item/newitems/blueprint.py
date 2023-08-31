from typing import List


from poe.item.newitems.base_item_model import Item

class Blueprint(Item):

    @property
    def area_level(self) -> int:
        for prop in self.properties:
            if prop.name == "Area Level":
                return int(prop.values[0][0])
        return None

    @property
    def blueprint_type(self) -> str:
        for prop in self.properties:
            if prop.name == "Heist Target: {0}":
                return prop.values[0][0]
        return None

    @property
    def wings(self):
        wings_property = [p for p in self.properties if "Wings Revealed" in p.name]
        if wings_property:
            return int(wings_property[0].values[0][0].split("/")[1])
        return None

    @property
    def hash_key(self):
        return [
            {'area_level': self.area_level, 'heist_type': self.blueprint_type, 'wings': self.wings},
            {'area_level': self.area_level, 'heist_type': self.blueprint_type, 'wings': None}
        ]
