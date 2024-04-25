import asyncio
from collections import defaultdict


class RatelimitCounter:
    def __init__(self, **kwargs):
        self.counts = defaultdict(int)

    def increment(self, key, rate_limit_period=60,incr=1):
        """Increment the rate limit count for a given key and schedule a decrement."""
        self.counts[key] += 1
        asyncio.create_task(self.decrement_after(key, rate_limit_period))

    async def decrement_after(self, key, delay):
        """Waits for the specified delay and then decrements the count for the key."""
        await asyncio.sleep(delay)
        self.counts[key] -= 1

    def __getitem__(self, key):
        """Get the current count for a key."""
        return self.counts.get(key, 0)
