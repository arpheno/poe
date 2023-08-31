from poe.item.newitems.base_item_model import Item


class Contract(Item):

    @property
    def extract_area_level_and_contract_type(self):
        area_level = None
        contract_type = None
        for prop in self.properties:
            if prop.name == "Area Level":
                area_level = int(prop.values[0][0])
            elif prop.name.startswith("Requires"):
                contract_type = prop.values[1][0]
        return {'area_level': area_level, 'contract_type': contract_type}

    @property
    def area_level(self):
        return self.extract_area_level_and_contract_type['area_level']

    @property
    def contract_type(self):
        return self.extract_area_level_and_contract_type['contract_type']

    @property
    def hash_key(self):
        return [{'area_level': self.area_level, 'heist_type': self.contract_type}]
