
import requests
from collections import defaultdict
from poe.constants import LEAGUE

def ask_ninja_exchange(type, league=LEAGUE):
    url = "https://poe.ninja/poe1/api/economy/exchange/current/overview"
    params = dict(type=type, league=league)
    print(f"Exchange {type}", end="")
    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        data = response.json()
        print(".", end="")
        
        # Map ids to names
        id_to_name = {item['id']: item['name'] for item in data.get('items', [])}
        
        return_value = defaultdict(list)
        for line in data.get('lines', []):
            item_id = line.get('id')
            name = id_to_name.get(item_id)
            if name:
                # Normalize to match existing structure
                item_data = {
                    "name": name,
                    "type": type,
                    "chaosValue": line.get('primaryValue', 0),
                    "sparkline": line.get('sparkline', {}),
                    # Add other fields if needed
                }
                return_value[name].append(item_data)
        
        return dict(return_value)
    except Exception as e:
        print(f"Failed to fetch exchange data for {type}: {e}")
        return {}
