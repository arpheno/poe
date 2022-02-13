import requests

from constants import LEAGUE
from poe.trade.headers import headers


def _call(tab_index):
    url = "https://www.pathofexile.com/character-window/get-stash-items"
    params = dict(accountName="swozn", league=LEAGUE, tabIndex=tab_index, tabs=1)
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    tabs = data["tabs"]
    [current_tab] = [tab for tab in tabs if tab["i"] == tab_index]
    current_tab_name = current_tab["n"]
    for item in data["items"]:
        item["stashtab"] = current_tab_name
    return data["items"]
