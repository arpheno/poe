import asyncio

import yaml
from aiohttp import web, ClientSession
from urllib.parse import urlencode


class CacheManager:
    def __init__(self, base_url, default_update_interval=3600):
        self.base_url = base_url  # Configurable base URL
        self.default_update_interval = default_update_interval  # Default interval for cache updates
        self.caches = {}  # A generic cache dictionary
        self.update_tasks = {}  # Tasks for periodic updates

    async def fetch_and_cache_data(self, endpoint, params):
        # Serialize parameters to create a unique key
        param_str = urlencode(sorted(params.items()))
        full_url = f"{self.base_url}/{endpoint}?{param_str}"
        async with ClientSession() as session:
            async with session.get(full_url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Cache data using endpoint and parameter string as key
                    self.caches[(endpoint, param_str)] = data
                    print(f"Cache updated for {endpoint} with params {param_str}")

    async def start_update_task(self, endpoint, params):
        param_str = urlencode(sorted(params.items()))
        if (endpoint, param_str) not in self.update_tasks:
            async def update_task():
                while True:
                    await asyncio.sleep(self.default_update_interval)
                    await self.fetch_and_cache_data(endpoint, params)

            self.update_tasks[(endpoint, param_str)] = asyncio.create_task(update_task())
            print(f"Started periodic update for endpoint: {endpoint} with params {param_str}")

    async def handle_request(self, request):
        endpoint = request.match_info['endpoint']
        params = dict(request.query)

        # Serialize parameters to use as cache key
        param_str = urlencode(sorted(params.items()))
        if (endpoint, param_str) not in self.caches:
            print(f"Data not found for {endpoint} with params {param_str}")
            await self.fetch_and_cache_data(endpoint, params)
            await self.start_update_task(endpoint, params)

        # Return the cached response
        cached_response = self.caches.get((endpoint, param_str), None)
        if cached_response is not None:
            return web.json_response(cached_response)
        else:
            return web.Response(text="Data not found", status=404)


async def init_app():
    base_url = "https://poe.ninja"  # External configuration of the base URL
    update_interval = 3600  # Configurable update interval
    app = web.Application()
    cache_manager = CacheManager(base_url, update_interval)
    app.add_routes([web.get('/{endpoint:.*}', cache_manager.handle_request)])  # Capture all endpoints
    return app


def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    app = asyncio.run(init_app())
    web.run_app(app, port=8998)
