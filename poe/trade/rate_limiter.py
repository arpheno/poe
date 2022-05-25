import hashlib
import os
import time
from contextlib import contextmanager


@contextmanager
def limit_rate(key, limits, cache):
    for rate_limit in limits:
        limit, timeframe, timeout = rate_limit.split(":")
        rate_limit_key = f"{key}_{rate_limit}"
        while len(list(cache.scan_iter(f"{rate_limit_key}*"))) >= int(limit) - 1:
            time.sleep(0.3)
        own_key = f"{rate_limit_key}{hashlib.md5(os.urandom(32)).hexdigest()}"
        cache.set(own_key, 1)
        cache.expire(own_key, int(timeframe))
    yield
