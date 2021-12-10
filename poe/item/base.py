from poe.item.item import Item


class Base(Item):
    @property
    def influence(self):
        influence = sorted(key for key,value in self.influences.items() if value)
        return influence