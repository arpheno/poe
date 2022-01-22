from poe.item.item import Item


class Base(Item):
    @property
    def influence(self):
        influence = sorted(key for key, value in self.influences.items() if value)
        return influence

    def match(self, candidates: list[dict]):
        conditions = [
            lambda x: str(x.get("variant")).lower() == ("/".join(self.influences) or "none"),
            lambda x: x["levelRequired"] == self.ilvl,
        ]
        for candidate in candidates:
            if all(f(candidate) for f in conditions):
                return candidate
        return None
