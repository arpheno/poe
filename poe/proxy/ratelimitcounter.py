import asyncio
import logging
import time
from collections import defaultdict
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class RatelimitCounter:
    def __init__(self,log_interval=10, **kwargs):
        self.counts = defaultdict(int)
        self.log_interval = log_interval
    def increment(self, key, rate_limit_period=60,incr=1):
        """Increment the rate limit count for a given key and schedule a decrement."""
        self.counts[key] += incr
        asyncio.create_task(self.decrement_after(key, rate_limit_period,incr=incr))

    async def decrement_after(self, key, delay, incr=1):
        """Waits for the specified delay and then decrements the count for the key."""
        logger.debug(f"Scheduled to decrement {key} by {incr} after {delay} seconds")
        await asyncio.sleep(delay)
        self.counts[key] -= incr
        logger.debug(f"Decremented for {key} by {incr} after {delay} seconds")

    def __getitem__(self, key):
        """Get the current count for a key."""
        return self.counts.get(key, 0)
    def __setitem__(self, key, value):
        """Set the current count for a key."""
        self.counts[key] = value
    def update(self,other):
        self.counts.update(other)

    async def log_counts_periodically(self):
        """Log the counts dictionary at regular intervals."""
        while True:
            logger.info(f"Current counts: {dict(self.counts)}")
            await asyncio.sleep(self.log_interval)
