from typing import List

from poe.item.item import Item


class SkillGem(Item):
    @property
    def level(self):
        level = self.extract_property('Level')['values'][0][0].strip('%+()Max')
        return int(level)
    @property
    def quality(self):
        try:
            level = self.extract_property('Quality')['values'][0][0].strip('%+()Max')
            return int(level)
        except:
            return 0

    def match(self, candidates: list[dict]):
        conditions = [
            lambda x: x["gemLevel"] == self.level,
            lambda x: x.get("corrupted", False) == self.corrupted,
            lambda x: x.get("gemQuality", 0) == self.quality,
        ]
        for candidate in candidates:
            if all(f(candidate) for f in conditions):
                return candidate
        if self.quality < 20 or self.level < 5:
            for candidate in candidates:
                if all(f(candidate) for f in conditions[:-1]):
                    return candidate
        if self.quality == 20:
            # this can return multiple versions of the gem i.e: lvl 1 and lvl 20
            # so we select the least valuable one
            return [candidate for candidate in candidates if all(f(candidate) for f in conditions[1:])][-1]

        print(
            f"Couldn't find match for {self.name} {self.level} {self.quality} {'Corrupted' if self.corrupted else ''}",
            end=" ",
        )
        approximate_match = candidates[-1]
        print(
            f"Using {self.name}, "
            f"{approximate_match.get('gemLevel',0)} "
            f"{approximate_match.get('gemQuality',0)} instead"
        )
        return approximate_match
