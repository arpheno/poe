import pandas as pd


class InventoryCreator:
    def create_inventory(self, items):
        df = pd.DataFrame(
            [
                dict(
                    config_value=item.config_value,
                    simple_value=item.simple_value,
                    type=item.type,
                    type_line=item.typeLine,
                    initial_price=item.price,
                    shoplink_template=item.shoplink_template,
                    stack_size=item.stack_size,
                )
                for item in items
            ]
        )
        inventory = df[~df["type"].isin([None]) & (df.config_value > 0)]
        return inventory
