import requests
import os
from typing import Optional, Dict, Any

PROXY_URL = os.getenv("POE_PROXY_URL", "http://localhost:8999")

class PoEClient:
    def __init__(self, proxy_url: str = PROXY_URL):
        self.proxy_url = proxy_url
        self.session = requests.Session()
        # Add headers if needed (User-Agent is handled by proxy usually, but good to have)
        self.session.headers.update({
            "User-Agent": "OAuth poe-trade-search/1.0.0 (contact: swozny@gmail.com)",
        })

    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Make a GET request to the PoE API via the proxy.
        endpoint: e.g. "/api/trade/search/Settlers"
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
            
        url = f"{self.proxy_url}{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            raise

    def post(self, endpoint: str, json: Optional[Dict] = None) -> requests.Response:
        """
        Make a POST request to the PoE API via the proxy.
        """
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
            
        url = f"{self.proxy_url}{endpoint}"
        try:
            response = self.session.post(url, json=json)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error posting to {url}: {e}")
            raise

# Singleton instance
client = PoEClient()
