from poe.item.items.item import Item


class BaseType(Item):
    @property
    def influence(self):
        influence = sorted(key for key, value in self.influences.items() if value)
        return influence

    def match(self, prices: dict):
        candidates = (
            prices.get(self.name)
            or prices.get(self.typeLine)
            or prices.get(self.baseType)
        )
        conditions = [
            lambda x: str(x.get("variant")).lower()
            == ("/".join(self.influences) or "none"),
            lambda x: x["levelRequired"] == self.ilvl,
        ]
        for candidate in candidates:
            if all(f(candidate) for f in conditions):
                return candidate
        return None
