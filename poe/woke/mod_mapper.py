import re

import pandas as pd
from pydantic import BaseModel


class Mod(BaseModel):
    id: str
    text: str
    regex_pattern: str
    type: str
    value: int


class ModMapper:
    def __init__(self, trade_keys):
        self.mod_mapping = pd.DataFrame(
            [item for items in pd.DataFrame(pd.DataFrame(trade_keys['result'])['entries'])['entries'].tolist() for item
             in
             items])
        self.mod_mapping['regex_pattern'] = self.mod_mapping['text'].str.replace('[+-]', r'\\\g<0>', regex=True)
        self.mod_mapping['regex_pattern'] = self.mod_mapping['regex_pattern'].apply(lambda x: re.escape(x).replace(r'\#', r'(\d+)').replace(r'\\\+', r'\\+').replace(r'\\\-', r'\\-'))

    def map_mods(self, mod_type, mods_list) -> [Mod]:
        mods = []
        mod_mapping_filtered = self.mod_mapping.query(f'type=="{mod_type}"')
        for mod in mods_list:
            for _, row in mod_mapping_filtered.iterrows():
                if found := re.search(f'^{row["regex_pattern"]}$', mod):
                    #Sometimes the value is not present in the mod, then just do 1
                    try:
                        mods.append(Mod(**row.to_dict(), value=int(found.group(1))))
                    except:
                        mods.append(Mod(**row.to_dict(), value=1))
                    break
            else:
                print(f"Mod {mod} not found in mapping")
        return mods
