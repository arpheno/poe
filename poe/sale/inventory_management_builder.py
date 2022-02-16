from fractions import Fraction

from poe.item.item_builder import ItemBuilder
from poe.sale.inventory_creator import InventoryCreator
from poe.sale.seller import Seller
from poe.sale.up_pricer import UpPricer
from poe.sale.inventory_management import InventoryManagement
from poe.trade.forum_updater import ForumUpdater


def turn_to_fraction(self):
    return Fraction(self.up_priced_value_fx / self.stack_size).limit_denominator(self.stack_size)


def build_inventory_management(*, prices, valuations, price_base_by_type={}, price_base=1,cleaning_rules=[],thread=''):
    item_builder = ItemBuilder(prices, valuations)
    inventory_creator = InventoryCreator()
    up_pricer = UpPricer(price_base_by_type, price_base)
    seller = Seller(turn_to_fraction=turn_to_fraction, up_price=up_pricer.up_price, cleaning_rules=cleaning_rules)
    forum_updater=ForumUpdater(thread)
    use_case = InventoryManagement(item_builder, inventory_creator, seller,forum_updater)
    return use_case
