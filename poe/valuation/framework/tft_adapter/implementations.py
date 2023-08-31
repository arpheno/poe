from poe.valuation.framework.tft_adapter.base_data_model import TimestampedWholesalePrices
from poe.valuation.framework.valuation import Valuation


class BulkBeasts(TimestampedWholesalePrices):
    # implementation specific to bulk-beasts.json
    pass


class BulkBreach(TimestampedWholesalePrices):
    # implementation specific to bulk-breach.json
    pass


class BulkCompasses(TimestampedWholesalePrices):
    # implementation specific to bulk-compasses.json
    def as_valuations(self):
        items = super(BulkCompasses, self).as_valuations()
        for item in items:
            item.tags.append('compass')
        return items




class BulkExpedition(TimestampedWholesalePrices):
    # implementation specific to bulk-expedition.json
    def as_valuations(self):
        currencies = TimestampedWholesalePrices(timestamp=self.timestamp,
                                                data=[v for v in self.data if len(v.name.split()) > 2]).as_valuations()
        logbooks = [
            Valuation({'area_level': 83, 'logbook_faction': item.name}, estimate=item.chaos, timestamp=self.timestamp,
                      info='tft_bulk_prices',
                      tags=['sellable', 'purchasable', 'bulk']) for item in self.data]
        return currencies + logbooks


class BulkHeist(TimestampedWholesalePrices):
    # implementation specific to bulk-heist.json
    def as_valuations(self):
        items = [
            Valuation({'area_level': 83, 'heist_type': item.name,'wings':None}, estimate=item.chaos, timestamp=self.timestamp,
                      info='tft_bulk_prices',
                      tags=['sellable', 'purchasable', 'bulk']) for item in self.data]
        return items


class BulkInvitation(TimestampedWholesalePrices):
    # implementation specific to bulk-invitation.json
    pass


class BulkLegionJewels(TimestampedWholesalePrices):
    # implementation specific to bulk-legion-jewels.json
    pass


class BulkLifeforce(TimestampedWholesalePrices):
    # implementation specific to bulk-lifeforce.json
    pass


class BulkMaps(TimestampedWholesalePrices):
    # implementation specific to bulk-maps.json
    pass


class BulkSets(TimestampedWholesalePrices):
    # implementation specific to bulk-sets.json
    pass


class BulkSimulacrum(TimestampedWholesalePrices):
    # implementation specific to bulk-simulacrum.json
    pass


class BulkStackedDeck(TimestampedWholesalePrices):
    # implementation specific to bulk-stacked-deck.json
    pass


class BulkVessel(TimestampedWholesalePrices):
    # implementation specific to bulk-vessel.json
    pass


class BulkWatchersEye(TimestampedWholesalePrices):
    # implementation specific to bulk-watcher's-eye.json
    pass


class Hideout(TimestampedWholesalePrices):
    # implementation specific to hideout.json
    pass


class Service(TimestampedWholesalePrices):
    # implementation specific to service.json
    pass
