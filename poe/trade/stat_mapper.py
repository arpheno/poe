"""
Stat Mapper for Path of Exile Trade API

This module fetches and provides mappings between human-readable affix text
and the internal stat IDs used by the Path of Exile trade API.
"""

import requests
from typing import Dict, List, Optional
import pandas as pd
from functools import lru_cache


class StatMapper:
    """
    Handles mapping between human-readable stat text and trade API stat IDs.
    
    Example:
        mapper = StatMapper()
        stat_id = mapper.text_to_id("# additional Physical Damage Reduction")
        # Returns: "explicit.stat_3771516363"
        
        # Or search with fuzzy matching
        matches = mapper.search("physical reduction")
    """
    
    def __init__(self, league: str = "Settlers"):
        """
        Initialize the stat mapper.
        
        Args:
            league: The current league name (default: "Settlers")
        """
        self.league = league
        self._stats_data: Optional[Dict] = None
        self._text_to_id_map: Optional[Dict[str, str]] = None
        self._id_to_text_map: Optional[Dict[str, str]] = None
        self._df: Optional[pd.DataFrame] = None
    
    @property
    def stats_data(self) -> Dict:
        """Lazy load the stats data from the API."""
        if self._stats_data is None:
            self._fetch_stats()
        return self._stats_data
    
    @property
    def df(self) -> pd.DataFrame:
        """Get a pandas DataFrame of all stats."""
        if self._df is None:
            self._build_dataframe()
        return self._df
    
    def _fetch_stats(self):
        """Fetch stats from the PoE trade API."""
        from poe.trade.headers import headers
        
        url = "https://www.pathofexile.com/api/trade/data/stats"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        self._stats_data = response.json()
    
    def _build_dataframe(self):
        """Build a pandas DataFrame from the stats data."""
        # Extract all entries from all stat groups
        all_entries = []
        for group in self.stats_data.get('result', []):
            entries = group.get('entries', [])
            for entry in entries:
                # Add the group label for context
                entry_with_group = entry.copy()
                entry_with_group['group'] = group.get('label', 'unknown')
                all_entries.append(entry_with_group)
        
        self._df = pd.DataFrame(all_entries)
        
        # Build the mapping dictionaries
        self._text_to_id_map = dict(zip(self._df['text'], self._df['id']))
        self._id_to_text_map = dict(zip(self._df['id'], self._df['text']))
    
    def text_to_id(self, text: str) -> Optional[str]:
        """
        Convert human-readable stat text to stat ID.
        
        Args:
            text: The exact stat text as shown in the trade UI
            
        Returns:
            The stat ID (e.g., "explicit.stat_3771516363") or None if not found
        """
        if self._text_to_id_map is None:
            self._build_dataframe()
        return self._text_to_id_map.get(text)
    
    def id_to_text(self, stat_id: str) -> Optional[str]:
        """
        Convert stat ID to human-readable text.
        
        Args:
            stat_id: The internal stat ID (e.g., "explicit.stat_3771516363")
            
        Returns:
            The human-readable stat text or None if not found
        """
        if self._id_to_text_map is None:
            self._build_dataframe()
        return self._id_to_text_map.get(stat_id)
    
    def search(self, query: str, group: Optional[str] = None, 
               limit: int = 20) -> pd.DataFrame:
        """
        Search for stats matching a query string.
        
        Args:
            query: Search text (case-insensitive substring match)
            group: Optional filter by stat group (e.g., 'explicit', 'implicit')
            limit: Maximum number of results to return
            
        Returns:
            DataFrame with matching stats
        """
        df = self.df.copy()
        
        # Filter by group if specified
        if group:
            df = df[df['group'].str.contains(group, case=False, na=False)]
        
        # Search in text field
        mask = df['text'].str.contains(query, case=False, na=False)
        results = df[mask].head(limit)
        
        return results[['id', 'text', 'type', 'group']]
    
    def get_explicit_stats(self, query: Optional[str] = None) -> pd.DataFrame:
        """
        Get explicit (affix) stats, optionally filtered by query.
        
        Args:
            query: Optional search query
            
        Returns:
            DataFrame with explicit stats
        """
        df = self.df[self.df['type'] == 'explicit']
        
        if query:
            mask = df['text'].str.contains(query, case=False, na=False)
            df = df[mask]
        
        return df[['id', 'text']]
    
    def get_implicit_stats(self, query: Optional[str] = None) -> pd.DataFrame:
        """
        Get implicit stats, optionally filtered by query.
        
        Args:
            query: Optional search query
            
        Returns:
            DataFrame with implicit stats
        """
        df = self.df[self.df['type'] == 'implicit']
        
        if query:
            mask = df['text'].str.contains(query, case=False, na=False)
            df = df[mask]
        
        return df[['id', 'text']]
    
    def build_search_query(self, stat_filters: List[Dict]) -> Dict:
        """
        Build a trade search query from stat filters.
        
        Args:
            stat_filters: List of dicts with 'text' or 'id', and optional 'min'/'max' values
                Example: [
                    {'text': '# additional Physical Damage Reduction', 'min': 3},
                    {'id': 'explicit.stat_123', 'max': 50}
                ]
        
        Returns:
            A properly formatted stats query for the trade API
        """
        filters = []
        
        for stat in stat_filters:
            # Get the stat ID if text was provided
            if 'text' in stat:
                stat_id = self.text_to_id(stat['text'])
                if not stat_id:
                    raise ValueError(f"Stat not found: {stat['text']}")
            elif 'id' in stat:
                stat_id = stat['id']
            else:
                raise ValueError("Each stat filter must have either 'text' or 'id'")
            
            # Build the filter
            filter_dict = {'id': stat_id}
            if 'min' in stat:
                filter_dict['value'] = {'min': stat['min']}
            if 'max' in stat:
                if 'value' not in filter_dict:
                    filter_dict['value'] = {}
                filter_dict['value']['max'] = stat['max']
            
            filters.append(filter_dict)
        
        return {
            'query': {
                'stats': [
                    {
                        'type': 'and',
                        'filters': filters
                    }
                ]
            }
        }


# Convenience function for quick lookups
@lru_cache(maxsize=1)
def get_stat_mapper(league: str = "Settlers") -> StatMapper:
    """Get a cached StatMapper instance."""
    return StatMapper(league=league)


if __name__ == "__main__":
    # Example usage
    mapper = StatMapper()
    
    print("=== Example 1: Text to ID ===")
    text = "#% additional Physical Damage Reduction"
    stat_id = mapper.text_to_id(text)
    print(f"Text: {text}")
    print(f"ID: {stat_id}")
    
    print("\n=== Example 2: ID to Text ===")
    print(f"ID: explicit.stat_3771516363")
    print(f"Text: {mapper.id_to_text('explicit.stat_3771516363')}")
    
    print("\n=== Example 3: Search ===")
    results = mapper.search("physical reduction", limit=5)
    print(results)
    
    print("\n=== Example 4: Build Query ===")
    query = mapper.build_search_query([
        {'text': '#% additional Physical Damage Reduction', 'min': 3}
    ])
    print(query)
