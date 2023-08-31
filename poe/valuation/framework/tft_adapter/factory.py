from poe.valuation.framework.tft_adapter.base_data_model import TimestampedWholesalePrices
from poe.valuation.framework.tft_adapter.implementations import BulkBeasts, BulkBreach, BulkCompasses, BulkExpedition, \
    BulkHeist, BulkInvitation, BulkLegionJewels, BulkLifeforce, BulkMaps, BulkSets, BulkSimulacrum, BulkStackedDeck, \
    BulkVessel, BulkWatchersEye, Hideout, Service


class TimestampedWholesalePricesFactory:
    @staticmethod
    def create(file_name):
        implementations = {
            "bulk-beasts.json": BulkBeasts,
            "bulk-breach.json": BulkBreach,
            "bulk-compasses.json": BulkCompasses,
            "bulk-expedition.json": BulkExpedition,
            "bulk-heist.json": BulkHeist,
            "bulk-invitation.json": BulkInvitation,
            "bulk-legion-jewels.json": BulkLegionJewels,
            "bulk-lifeforce.json": BulkLifeforce,
            "bulk-maps.json": BulkMaps,
            "bulk-sets.json": BulkSets,
            "bulk-simulacrum.json": BulkSimulacrum,
            "bulk-stacked-deck.json": BulkStackedDeck,
            "bulk-vessel.json": BulkVessel,
            "bulk-watcher's-eye.json": BulkWatchersEye,
            "hideout.json": Hideout,
            "service.json": Service,
        }
        # Return TimestampedWholesalePrices as the default implementation
        return implementations.get(file_name, TimestampedWholesalePrices)
