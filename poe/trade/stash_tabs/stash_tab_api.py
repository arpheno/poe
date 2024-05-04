import requests

from trade.headers import headers


class StashTabAPI:
    def __init__(self, account_name, league, base_url="https://www.pathofexile.com"):
        self.account_name = account_name
        self.league = league
        self.base_url = f'{base_url}/character-window/get-stash-items'

    def fetch_tab_data(self, tab_index):
        params = {
            "accountName": self.account_name,
            "league": self.league,
            "tabIndex": tab_index,
            "tabs": 1
        }
        response = requests.get(self.base_url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
