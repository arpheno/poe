from typing import List

import pandas as pd

from poe.bulk.report_processing.amount_fixer import fix_amount
from poe.bulk.report_processing.name_matcher import match_names


def process_report(stuff: List[List[str]]):
    df = pd.DataFrame(
        stuff,
        columns=[
            "amount",
            "name",
            "ninja_price",
            "asked_price",
            "percentage",
            "total_chaos",
            "total_exalt",
        ],
    )
    df["amount"] = df["amount"].map(fix_amount)
    df["name"] = df.name.map(match_names)
    return
