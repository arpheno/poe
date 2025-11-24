"""
Example: Using the Stat Mapper for PoE Trade Search

This script demonstrates how to use the StatMapper to:
1. Find stat IDs from human-readable text
2. Search for stats
3. Build trade API queries
"""

from poe.trade.stat_mapper import StatMapper

# Initialize the mapper
mapper = StatMapper()

# === Example 1: Find the stat ID for a known text ===
print("=== Example 1: Text to ID lookup ===")
stat_text = "#% additional Physical Damage Reduction"
stat_id = mapper.text_to_id(stat_text)
print(f"Looking for: '{stat_text}'")
print(f"Found ID: {stat_id}")
print()

# === Example 2: Reverse lookup (ID to text) ===
print("=== Example 2: ID to Text lookup ===")
stat_id = "explicit.stat_3771516363"
stat_text = mapper.id_to_text(stat_id)
print(f"Looking for ID: {stat_id}")
print(f"Found text: '{stat_text}'")
print()

# === Example 3: Search for stats ===
print("=== Example 3: Search for 'physical reduction' ===")
results = mapper.search("physical reduction", limit=10)
print(results.to_string(index=False))
print()

# === Example 4: Get all explicit stats with 'life' ===
print("=== Example 4: All explicit stats containing 'life' ===")
life_stats = mapper.get_explicit_stats("life")
print(f"Found {len(life_stats)} stats")
print(life_stats.head(10).to_string(index=False))
print()

# === Example 5: Build a complete trade search query ===
print("=== Example 5: Build a trade search query ===")
# This creates the same query as shown in your screenshot
query = mapper.build_search_query([
    {
        'text': '#% additional Physical Damage Reduction',
        'min': 3  # Looking for at least 3% additional physical reduction
    }
])

print("Query structure:")
import json
print(json.dumps(query, indent=2))
print()

# === Example 6: Multiple stats query ===
print("=== Example 6: Search with multiple stats ===")
multi_stat_query = mapper.build_search_query([
    {'text': '+# to maximum Life', 'min': 70},
    {'text': '+#% to Fire Resistance', 'min': 30},
])

print(json.dumps(multi_stat_query, indent=2))
print()

# === Example 7: Browse all stat categories ===
print("=== Example 7: Available stat groups ===")
groups = mapper.df['group'].unique()
for group in groups[:10]:  # Show first 10 groups
    count = len(mapper.df[mapper.df['group'] == group])
    print(f"{group}: {count} stats")
print()

# === Example 8: Using in a real search ===
print("=== Example 8: Complete search example ===")
import requests
from poe.trade.headers import headers

# Build the query for a specific item with specific stats
search_query = {
    "query": {
        "status": {
            "option": "online"  # Only show online sellers
        },
        "stats": [
            {
                "type": "and",
                "filters": [
                    {"id": mapper.text_to_id("+# to maximum Life"), "value": {"min": 70}},
                    {"id": mapper.text_to_id("+#% to Fire Resistance"), "value": {"min": 30}},
                ]
            }
        ]
    },
    "sort": {
        "price": "asc"
    }
}

print("Search query:")
print(json.dumps(search_query, indent=2))

# Note: To actually run this search, you would do:
# response = requests.post(
#     "https://www.pathofexile.com/api/trade/search/Settlers",
#     json=search_query,
#     headers=headers
# )
# results = response.json()
