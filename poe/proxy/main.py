import asyncio
import functools
import logging
from pprint import pprint
from typing import Callable, Coroutine

import yaml

from proxy.proxy_handler import ProxyHandler
from proxy.proxy_server import ProxyServer
from proxy.rate_limit_parser import parse_rate_limit_headers, RateLimit
from proxy.ratelimitcounter import RatelimitCounter

logger = logging.getLogger(__name__)


def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


DEFAULT_POLICY = RateLimit('default', 'default', 2, 5, 60)


class RateLimiter:
    def __init__(self, counter):
        self.counter = counter
        self.policy_map = {}

    def __call__(self, func: Callable) -> Callable:
        async def wrapper(request):
            # Wait until the rate limit allows proceeding with the request
            await self.wait_until_allowed(request)

            # Proceed with the function call once allowed
            response = await func(request)

            # Check if the response status is 429 and handle accordingly
            if response.status == 429:
                await self.handle_rate_limited_response(request, response)

            # Check if new policies need to be updated from the response headers
            if not self.cache_key(request) in self.policy_map:
                print(f'New policies for {self.cache_key(request)}')
                await self.update_policies_from_response(request, response)
            else:
                print(f'Policies for {self.cache_key(request)} already exist')

            return response

        return wrapper

    def cache_key(self, request):
        # Cache key is based on the method and the first 4 path components
        # This might need to be adjusted based on the API being proxied
        # Also I have no idea what I am doing, I blame ChatGPT.
        return f'{request.method}:{"/".join(request.path.split("/")[:4])}'

    async def handle_rate_limited_response(self, request, response):
        """Handle actions specific to receiving a 429 rate limited response."""
        retry_after = response.headers.get('Retry-After')
        if retry_after:
            retry_after = int(retry_after)
            policy = self.policy_map.get(request.path, [RateLimit('default', 'default', 10, 60, 60)])[0]
            self.counter.increment(policy, retry_after + 1, incr=retry_after)

    async def update_policies_from_response(self, request, response):
        """Update rate limiting policies from response headers."""
        policies = parse_rate_limit_headers(response.headers)
        self.policy_map[self.cache_key(request)] = policies

    async def wait_until_allowed(self, request):
        """Wait until the rate limit is no longer exceeded."""
        policies = self.policy_map.get(request.path, [RateLimit('default', 'default', 10, 60, 60)])
        while any(limit := key if (self.counter[key] > key.requests - 2) else None for key in policies):
            await asyncio.sleep(1)
            print(f'Rate limit exceeded for {request.path} because of {limit}')
        # Increment the rate limit counter state
        for policy in policies:
            self.counter.increment(policy)


if __name__ == '__main__':
    config = load_config('config.yaml')
    ratelimit_counter = RatelimitCounter(**config.get('ratelimit_counter', {}))
    rate_limiter = RateLimiter(ratelimit_counter, **config.get('rate_limiter', {}))
    proxy_handler = ProxyHandler(**config['proxy_handler'])
    server = ProxyServer(rate_limiter(proxy_handler.forward_request), **config['proxy_server'])

    asyncio.run(server.run())
