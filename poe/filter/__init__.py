import pandas as pd
import re
import ast
from bs4 import BeautifulSoup

import requests
from requests import Response

from poe.trade.headers import headers
class ItemModsApi:
    def __init__(self, base_url="https://raw.githubusercontent.com/PathOfBuildingCommunity/PathOfBuilding/dev/src/Data/"):
        self.base_url = base_url
        self.path = 'ModItem.lua'

    def fetch_item_mods(self):
        response = self._fetch_item_mods()
        mods = self._parse_item_mods(response)
        return mods
    def _parse_item_mods(self, response: Response) -> pd.DataFrame:
        lua_data = response.text
        lua_data = lua_data[lua_data.find('return'):]
        # Remove the 'return' statement and leading/trailing braces
        lua_data = lua_data.replace('return ', '').strip()
        lua_data = lua_data[1:-1].strip()

        # Replace Lua table notation with Python dictionary notation
        lua_data = re.sub(r'\[\"(.*?)\"\]', r'"\1"', lua_data)
        lua_data = re.sub(r'\"(\w+)\"\s*:', r'"\1":', lua_data)
        lua_data = re.sub(r'(\w+)\s*:', r'"\1":', lua_data)
        print(lua_data)
        # Convert the string to a Python dictionary
        data_dict = ast.literal_eval(lua_data)

        # Print the resulting dictionary
        import pprint
        pprint.pprint(data_dict)

    def _fetch_item_mods(self):
        response = requests.get(f'{self.base_url}/{self.path}', headers=headers)
        response.raise_for_status()
        print(f'Item mods fetched, status code: {response.status_code}')
        return response

class FilterApi:
    def __init__(self, base_url="https://www.pathofexile.com"):
        self.base_url = f'{base_url}/item-filter'

    def post_filter(self, data, name='gq7M0KSE'):
        response = requests.post(f'{self.base_url}/{name}', data=data, headers=headers)
        response.raise_for_status()
        print(f'Filter {name} created, status code: {response.status_code}')
        return response.json()
    def _load_filter(self, name='gq7M0KSE')-> Response:
        response = requests.get(f'{self.base_url}/{name}', headers=headers)
        response.raise_for_status()
        print(f'Filter {name} fetched, status code: {response.status_code}')
        return response
    def get_filter(self, name='gq7M0KSE')-> str:
        response = self._load_filter(name)
        filter = self._parse_filter_from_html(response)
        return filter
    def _parse_filter_from_html(self, response: Response) -> str:
        soup = BeautifulSoup(response.text, 'html.parser')
        filter_textarea = soup.find('textarea', {'name': 'filter'})

        if filter_textarea:
            loot_filter = filter_textarea.text
            print("Loot Filter extracted successfully:")
        else:
            print("Loot Filter textarea not found")
        return loot_filter


# if __name__ == '__main__':
    # filter_api = FilterApi()
    # print(filter_api.get_filter())
    # item_mods_api = ItemModsApi()
    # item_mods_api.fetch_item_mods()

from luaparser import ast

src = '''
return {
    ["Strength1"] = { type = "Suffix", affix = "of the Brute", "+(8-12) to Strength", statOrderKey = "1044", statOrder = { 1044 }, level = 1, group = "Strength", weightKey = { "ring", "amulet", "belt", "str_armour", "str_dex_armour", "str_int_armour", "str_dex_int_armour", "sword", "mace", "sceptre", "staff", "axe", "default", }, weightVal = { 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 0 }, modTags = { "attribute" }, },
    ["Strength2"] = { type = "Suffix", affix = "of the Wrestler", "+(13-17) to Strength", statOrderKey = "1044", statOrder = { 1044 }, level = 11, group = "Strength", weightKey = { "ring", "amulet", "belt", "str_armour", "str_dex_armour", "str_int_armour", "str_dex_int_armour", "sword", "mace", "sceptre", "staff", "axe", "default", }, weightVal = { 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 0 }, modTags = { "attribute" }, },
}
'''


data = src[src.find('{')+1:-src[::-1].find('}')-1].strip().splitlines()
data=data[0].strip()
data=data.replace('[', '')
data=data.replace(']', '')
data=data.replace(' = ','":')
data=data.replace('{ ', '{"')
data=data.replace(' }', '"}')
data=data.replace(', ', '","')
data=data.replace('""','"')
data=data.replace(',"}""','"}')

data=data.replace(',"}""','"}')
data=data.replace(',"}"', '"}')
data=data.replace('""','"')
data= data.replace('}"', '}')
data= data.replace(',"}', '}')
data= data.replace('}}', '}')
# for n in "0123456789":
#     data=data.replace(n+'"', n)
#     data = data.replace('"'+n, n)
print(data)
pseudo_python = f'{data}'
# read this string as a dictionary
data_dict = eval(pseudo_python)