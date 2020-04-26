import glob
import pandas as pd


def read_directory(directory):
    return pd.concat([pd.read_parquet(path) for path in glob.glob(f"{directory}/*")], ignore_index=True)


def construct_timeline():
    df = read_directory("market_depth")
    df["diffstock"] = df.sort_values("timestamp").groupby(["id"]).diff()["stock"]
    timeline = (
        df.dropna()[df["diffstock"] < 0]
        .groupby(["timestamp", "pay_currency", "get_currency"])
        .apply(lambda group: (group.diffstock * group.price).sum() / group.diffstock.sum())
    )
    return timeline


def get_most_recent_price(timeline):
    return timeline.reset_index().sort_values("timestamp").groupby(["pay_currency", "get_currency"]).last()
