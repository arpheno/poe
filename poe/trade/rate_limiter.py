
import hashlib
import os
import time
from contextlib import contextmanager

# from redislite import Redis
#
#
# class RateLimiter:
#     def __init__(self, *keys, cache=Redis()):
#         self.keys = keys
#         self.cache = cache
#
#
#     def __enter__(self):
#         if self.limit is None or self.timeframe is None or self.timeout is None:
#             raise ValueError('Rate limit headers not set')
#         with limit_rate(key,limits,self.cache):
#             yield
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass
#
#     def set_limits(self, response):
#         rate_limit_header = response.headers.get(self.key)
#         if rate_limit_header:
#             self.limit, self.timeframe, self.timeout = map(int, rate_limit_header.split(':'))
#         else:
#             raise ValueError('Rate limit headers not found in response')
@contextmanager
def limit_rate(key, limits, cache):
    for rate_limit in limits:
        limit, timeframe, timeout = rate_limit.split(":")
        rate_limit_key = f"{key}_{rate_limit}"
        while len(list(cache.scan_iter(f"{rate_limit_key}*"))) >= int(limit) - 1:
            print('.',end='')
            time.sleep(0.3)
        own_key = f"{rate_limit_key}{hashlib.md5(os.urandom(32)).hexdigest()}"
        cache.set(own_key, 1)
        cache.expire(own_key, int(timeframe))
    yield
