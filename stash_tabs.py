import requests

from constants import ssid
from item import Item


def get_currency_tab():
    return [Item(**line) for data in [_call(tab_index) for tab_index in range(16)] for line in data]

# @backoff.on_exception(backoff.expo,
#                       requests.exceptions.RequestException)
def _call(tab_index):
    url = "https://www.pathofexile.com/character-window/get-stash-items"
    headers = {"Cookie": f"POESESSID={ssid}"}
    params = dict(accountName="swozn", league="delirium", tabIndex=tab_index, tabs=1)
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data["items"]

