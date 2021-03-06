from pprint import pprint

import requests

from constants import ssid
from item import Item


def get_all_tabs():
    return [Item(stashtab=data[0], **items) for data in [_call(tab_index) for tab_index in range(20)] for items in data[1]]

# @backoff.on_exception(backoff.expo,
#                       requests.exceptions.RequestException)
def _call(tab_index):
    url = "https://www.pathofexile.com/character-window/get-stash-items"
    # cookies = {"POESSID":ssid,
    #            "__cfduid": "d18f7bd987ce2b3f98c02b05b92a782c31618165141",
    #            "cf_clearance": "7d322aa725fafce9ef1ebc8a26759033b127dd7f-1618777267-0-150"}

    headers = {
        'authority': 'www.pathofexile.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'cookie': '__cfduid=d18f7bd987ce2b3f98c02b05b92a782c31618165141; cf_clearance=7d322aa725fafce9ef1ebc8a26759033b127dd7f-1618777267-0-150; POESESSID=316a81f7acdf633a6c4dc420e77c0a90; _ga=GA1.2.1675387988.1618777334; _gid=GA1.2.715037690.1618777334',
    }
    params = dict(accountName="swozn", league="ultimatum", tabIndex=tab_index, tabs=1)
    response = requests.get(url,  params=params,headers=headers)
    response.raise_for_status()
    data = response.json()
    tabs = data['tabs']
    [current_tab]= [tab for tab in tabs if tab['i']==tab_index]
    return current_tab['n'],data["items"]
if __name__ == '__main__':
   pprint(_call(3))


