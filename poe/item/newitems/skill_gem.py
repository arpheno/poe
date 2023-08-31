from poe.item.newitems.base_item_model import Item


class SkillGem(Item):
    @property
    def level(self):
        level = self.extract_property("Level").values[0][0].strip("%+()Max")
        return int(level)

    @property
    def quality(self):
        try:
            level = self.extract_property("Quality").values[0][0].strip("%+()Max")
            return int(level)
        except:
            return 0

    @property
    def hash_key(self):
        return {"gem_level": self.level, "gem_quality": self.quality, "name": self.name}
