# Path of Exile Trade API - Stat Mapping Guide

## The Problem

When using the Path of Exile trade website, you see human-readable stat descriptions like:
- `#% additional Physical Damage Reduction`
- `+# to maximum Life`
- `Gain # Charge when you are Hit by an Enemy`

But when you search, the API uses internal stat IDs like:
- `explicit.stat_3771516363`
- `explicit.stat_3299347043`
- etc.

This makes it difficult to programmatically build search queries without knowing the mappings.

## The Solution

The Path of Exile trade API provides a **stats endpoint** that contains all the mappings:

```
https://www.pathofexile.com/api/trade/data/stats
```

This endpoint returns a JSON structure with all stat definitions organized by category (explicit, implicit, enchant, crafted, fractured, etc.).

## Response Structure

```json
{
  "result": [
    {
      "label": "Explicit",
      "entries": [
        {
          "id": "explicit.stat_3771516363",
          "text": "#% additional Physical Damage Reduction",
          "type": "explicit"
        },
        {
          "id": "explicit.stat_3299347043",
          "text": "+# to maximum Life",
          "type": "explicit"
        }
        // ... thousands more
      ]
    },
    {
      "label": "Implicit",
      "entries": [...]
    }
    // ... more categories
  ]
}
```

## Using the StatMapper Class

I've created a `StatMapper` class in `poe/trade/stat_mapper.py` to make this easy:

### Basic Usage

```python
from poe.trade.stat_mapper import StatMapper

# Initialize the mapper (automatically fetches data)
mapper = StatMapper()

# Convert text to ID
stat_id = mapper.text_to_id("#% additional Physical Damage Reduction")
# Returns: "explicit.stat_3771516363"

# Convert ID to text
text = mapper.id_to_text("explicit.stat_3771516363")
# Returns: "#% additional Physical Damage Reduction"
```

### Searching for Stats

```python
# Search for stats containing "physical reduction"
results = mapper.search("physical reduction", limit=10)
print(results)
#                         id                                  text          type     group
# explicit.stat_3771516363  #% additional Physical Damage Reduction  explicit  Explicit
# ...
```

### Building Trade Queries

```python
# Build a search query
query = mapper.build_search_query([
    {
        'text': '#% additional Physical Damage Reduction',
        'min': 3,
        'max': 5
    },
    {
        'text': '+# to maximum Life',
        'min': 70
    }
])

# Use it in a search
import requests
from poe.trade.headers import headers

response = requests.post(
    "https://www.pathofexile.com/api/trade/search/Settlers",
    json=query,
    headers=headers
)
```

### Filtering by Stat Type

```python
# Get all explicit (affix) stats
explicit_stats = mapper.get_explicit_stats()

# Get all implicit stats
implicit_stats = mapper.get_implicit_stats()

# Get explicit stats containing "life"
life_stats = mapper.get_explicit_stats("life")
```

### Access Raw Data

```python
# Get the full DataFrame
df = mapper.df
print(df.columns)
# ['id', 'text', 'type', 'group', 'option']

# Filter and analyze as needed
physical_stats = df[df['text'].str.contains('Physical', case=False)]
```

## Example: Recreating Your Search

Your screenshot shows searching for items with "Gain # Charge when you are Hit by an Enemy" with value 3.

Here's how to build that programmatically:

```python
from poe.trade.stat_mapper import StatMapper
import requests
from poe.trade.headers import headers

mapper = StatMapper()

# Build the query
search_query = {
    "query": {
        "status": {
            "option": "online"
        },
        "stats": [
            {
                "type": "and",
                "filters": [
                    {
                        "id": mapper.text_to_id("Gain # Charge when you are Hit by an Enemy"),
                        "value": {"min": 3, "max": 3}
                    }
                ]
            }
        ]
    },
    "sort": {
        "price": "asc"
    }
}

# Execute the search
response = requests.post(
    "https://www.pathofexile.com/api/trade/search/Keepers",
    json=search_query,
    headers=headers
)

results = response.json()
```

## Building a UI

Now that you have the mappings, you can build a user-friendly search interface:

1. **Load all stats** at startup using `StatMapper()`
2. **Create dropdowns/autocomplete** using `mapper.df['text'].tolist()`
3. **Group by category** using `mapper.df.groupby('group')`
4. **Convert user selections** to stat IDs when building queries

Example UI flow:
```python
# User selects from dropdown: "#% additional Physical Damage Reduction"
user_selection = "#% additional Physical Damage Reduction"
min_value = 3  # User enters minimum value

# Convert to query
stat_id = mapper.text_to_id(user_selection)
query_filter = {
    "id": stat_id,
    "value": {"min": min_value}
}
```

## Caching

The stats data is relatively large (~1.8MB) and doesn't change often. Consider:

1. **Caching the API response** locally
2. **Versioning your cache** (invalidate when new league starts)
3. **Using the provided `get_stat_mapper()` function** which uses `@lru_cache`

```python
from poe.trade.stat_mapper import get_stat_mapper

# This will cache the mapper instance
mapper = get_stat_mapper()
```

## Additional Notes

- The stats endpoint includes **all stat types**: explicit, implicit, enchant, crafted, fractured, pseudo, monster, delve, ultimatum, etc.
- Each stat has a `type` field indicating its category
- Some stats have an `option` field with multiple variants (e.g., different keystone allocations)
- The `#` character in text represents numeric values that can be min/max filtered

## See Also

- Example usage: `examples/stat_mapper_example.py`
- StatMapper implementation: `poe/trade/stat_mapper.py`
- Official PoE Trade: https://www.pathofexile.com/trade
