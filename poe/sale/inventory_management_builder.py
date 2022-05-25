from fractions import Fraction

from poe.item.item_builder import ItemBuilder
from poe.sale.inventory_creator import InventoryCreator
from poe.sale.layouters.base import Layouter
from poe.sale.seller import Seller
from poe.sale.up_pricer import Pricer
from poe.sale.inventory_management import InventoryManagement
from poe.trade.forum_updater import ForumUpdater


def build_inventory_management(
    *,
    prices,
    valuations,
    price_base_by_type={},
    price_base=1,
    cleaning_rules=[],
    thread="",
    min_trade_value=50,
):
    item_builder = ItemBuilder(prices, valuations)
    inventory_creator = InventoryCreator()
    exalt_value = prices["Exalted Orb"][0]["chaosValue"]
    pricer = Pricer(price_base_by_type, price_base)
    layouter = Layouter(exalt_value=exalt_value, min_trade_value=min_trade_value)
    seller = Seller(
        up_price=pricer.up_price, cleaning_rules=cleaning_rules, layouter=layouter
    )
    forum_updater = ForumUpdater(thread)
    use_case = InventoryManagement(
        item_builder, inventory_creator, seller, forum_updater
    )
    return use_case
