"""
Flask API for PoE Trade Search

Provides REST endpoints for the Vue frontend to execute trade searches.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

from poe.constants import LEAGUE
from poe.trade.headers import headers
from poe.trade.proxy_listings_resolver import ListingsResolver
from poe.trade.proxy_search_resolver import SearchResolver
from poe.woke.mod_mapper import ModMapper
from poe.woke.query_builder import build_query

app = Flask(__name__)
CORS(app)  # Enable CORS for Vue frontend

# Initialize components
PROXY_BASE_URL = "http://localhost:8999"
search_resolver = SearchResolver(league=LEAGUE, base_url=PROXY_BASE_URL)
listings_resolver = ListingsResolver(league=LEAGUE, base_url=PROXY_BASE_URL)

# Load trade keys once at startup
trade_keys = None
mod_mapper = None


def init_mod_mapper():
    global trade_keys, mod_mapper
    if trade_keys is None:
        trade_keys = requests.get(f'{PROXY_BASE_URL}/api/trade/data/stats', headers=headers).json()
        mod_mapper = ModMapper(trade_keys)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'league': LEAGUE})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get all available stats for building queries"""
    init_mod_mapper()
    return jsonify(trade_keys)


@app.route('/api/search', methods=['POST'])
def search():
    """
    Execute a trade search
    
    Request body:
    {
        "type": "Sapphire Flask",
        "prefixes": ["25% increased effect"],
        "suffixes": ["61% reduced Effect of Curses on you during Effect"],
        "misc": {
            "filters": {
                "corrupted": {"option": "false"},
                "quality": {"min": 20, "max": 20}
            }
        }
    }
    """
    try:
        init_mod_mapper()
        
        data = request.json
        item_type = data.get('type', '')
        prefixes = data.get('prefixes', [])
        suffixes = data.get('suffixes', [])
        misc = data.get('misc', {})
        
        # Combine prefixes and suffixes
        all_mods = prefixes + suffixes
        
        # Build the query
        query_args = {}
        
        if all_mods:
            query_args['mods'] = mod_mapper.map_mods('explicit', all_mods)
        
        if item_type:
            query_args['type'] = item_type
        
        if misc:
            query_args['misc'] = misc
        
        # Build and execute query
        query = build_query(**query_args)
        search_params = search_resolver.resolve(query)
        results = listings_resolver.resolve(search_params)
        
        # Extract prices
        listings = []
        for item in results.get('result', []):
            listing = {
                'id': item.get('id'),
                'item': item.get('item', {}),
                'listing': item.get('listing', {}),
            }
            
            # Extract price if available
            if 'price' in item.get('listing', {}):
                price = item['listing']['price']
                listing['chaos_price'] = to_chaos(price)
            
            listings.append(listing)
        
        return jsonify({
            'success': True,
            'count': len(listings),
            'results': listings,
            'query': query  # Include query for debugging
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/batch-search', methods=['POST'])
def batch_search():
    """
    Execute multiple searches in batch
    
    Request body:
    {
        "searches": [
            {
                "id": "unique-id-1",
                "type": "Sapphire Flask",
                "prefixes": ["25% increased effect"],
                "suffixes": ["61% reduced Effect of Curses on you during Effect"],
                "misc": {...}
            },
            ...
        ]
    }
    """
    try:
        init_mod_mapper()
        
        data = request.json
        searches = data.get('searches', [])
        
        results = []
        for search_config in searches:
            search_id = search_config.get('id', '')
            item_type = search_config.get('type', '')
            prefixes = search_config.get('prefixes', [])
            suffixes = search_config.get('suffixes', [])
            misc = search_config.get('misc', {})
            
            all_mods = prefixes + suffixes
            
            query_args = {}
            if all_mods:
                query_args['mods'] = mod_mapper.map_mods('explicit', all_mods)
            if item_type:
                query_args['type'] = item_type
            if misc:
                query_args['misc'] = misc
            
            try:
                query = build_query(**query_args)
                search_params = search_resolver.resolve(query)
                search_results = listings_resolver.resolve(search_params)
                
                listings = []
                for item in search_results.get('result', []):
                    if 'price' in item.get('listing', {}):
                        price = item['listing']['price']
                        listings.append({
                            'id': item.get('id'),
                            'chaos_price': to_chaos(price),
                            'listing': item.get('listing', {})
                        })
                
                results.append({
                    'id': search_id,
                    'success': True,
                    'type': item_type,
                    'prefixes': prefixes,
                    'suffixes': suffixes,
                    'count': len(listings),
                    'listings': listings
                })
            except Exception as e:
                results.append({
                    'id': search_id,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


def to_chaos(price: dict) -> float:
    """Convert price to chaos equivalent"""
    multiplier = 1 if price.get('currency') == 'chaos' else 100
    return price.get('amount', 0) * multiplier


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
