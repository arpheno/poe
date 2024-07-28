import asyncio
import logging
import uuid
from typing import Callable

import yaml

from proxy.proxy_handler import ProxyHandler
from proxy.proxy_server import ProxyServer
from proxy.rate_limit_parser import parse_rate_limit_headers, RateLimit, parse_for_timeout, check_rate_limit_violation
from proxy.ratelimitcounter import RatelimitCounter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, counter: RatelimitCounter):
        self.counter = counter
        self.policy_map = {}

    def __call__(self, func: Callable) -> Callable:
        async def wrapper(request):
            request_id = str(uuid.uuid4())  # Generate a unique request ID
            logger.info(f"Received Request with ID: {request_id}")  # Log the request ID

            # Wait until the rate limit allows proceeding with the request
            await self.wait_until_allowed(request)

            # Proceed with the function call once allowed
            response = await func(request)

            # Check if the response status is 429 and handle accordingly
            if response.status == 429:
                await self.handle_rate_limited_response(request, response)

            # Check if new policies need to be updated from the response headers
            await self.update_policies_from_response(request, response)
            logger.info(f"Finished Request with ID: {request_id}, returning response {response.status}")
            return response

        return wrapper

    def cache_key(self, request):
        # Cache key is based on the method and the first 4 path components
        # This might need to be adjusted based on the API being proxied
        # Also I have no idea what I am doing, I blame ChatGPT.
        return f'{request.method}:{"/".join(request.path.split("/")[:4])}'

    async def handle_rate_limited_response(self, request, response):
        """Handle actions specific to receiving a 429 rate limited response."""
        policy,timeout = check_rate_limit_violation(response.headers)
        logger.warn(f'Rate limited for {policy.policy}, blocking for {timeout}')
        self.counter.increment(policy, timeout+2, incr=1000)

    async def update_policies_from_response(self, request, response):
        """Update rate limiting policies from response headers."""
        policies, states = parse_rate_limit_headers(response.headers)
        if not self.cache_key(request) in self.policy_map:
            self.policy_map[self.cache_key(request)] = policies
        for key,value in states.items():
            if not self.counter[key] == value:
                logger.info(f"Divergent Server Response for {key} from {self.counter[key]} to {value}")
        self.counter.update(states)

    async def wait_until_allowed(self, request):
        """Wait until the rate limit is no longer exceeded."""
        policies = self.policy_map.get(self.cache_key(request), [RateLimit('default', 'default', 10, 60, 60)])
        while any(limit := key if (self.counter[key] > key.requests - 2) else None for key in policies):
            logger.info(
                f'Exceeded {limit.policy} at {self.cache_key(request)} {self.counter[limit]}/{limit.requests} requests per {limit.period}')
            await asyncio.sleep(1)
        for policy in policies:
            if self.counter[policy] > policy.requests - 3:
                logger.info( f'Proceeding {policy.policy} at {self.cache_key(request)} {self.counter[policy]}/{policy.requests} requests per {policy.period}')
        # Increment the rate limit counter state
        for policy in policies:
            self.counter.increment(policy, policy.period+0.1, incr=1)


def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    config = load_config('config.yaml')
    ratelimit_counter = RatelimitCounter(**config.get('ratelimit_counter', {}))
    ratelimit_counter.log_counts_periodically()
    rate_limiter = RateLimiter(ratelimit_counter, **config.get('rate_limiter', {}))
    proxy_handler = ProxyHandler(**config['proxy_handler'])
    server = ProxyServer(rate_limiter(proxy_handler.forward_request), **config['proxy_server'])

    asyncio.run(server.run())
