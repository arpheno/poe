from dataclasses import dataclass

from poe.item.item_builder import ItemBuilder
from poe.sale.inventory_creator import InventoryCreator
from poe.sale.seller import Seller
from poe.trade.forum_updater import ForumUpdater


@dataclass
class InventoryManagement:
    item_builder: ItemBuilder
    inventory_creator: InventoryCreator
    seller: Seller
    forum_updater: ForumUpdater

    def sales_proposition(self, inventory):
        sales_proposition = self.seller.sell(inventory)
        return sales_proposition

    def sell(self, sales_proposition):
        content = list(
            sales_proposition.apply(
                lambda row: row.shoplink_template.format(**row), axis=1
            )
        )
        forum_post = "\n".join(content)
        assert len(forum_post) < 49_999
        self.forum_updater.update_forum(forum_post)

    def create_inventory(self, raw_items):
        items = self.item_builder.build_items(raw_items)
        inventory = self.inventory_creator.create_inventory(items)
        return inventory
