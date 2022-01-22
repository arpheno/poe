import requests

from poe.trade.headers import headers


def _call(tab_index):
    url = "https://www.pathofexile.com/character-window/get-stash-items"
    params = dict(accountName="swozn", league="scourge", tabIndex=tab_index, tabs=1)

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    tabs = data["tabs"]
    [current_tab] = [tab for tab in tabs if tab["i"] == tab_index]
    return current_tab["n"], data["items"]