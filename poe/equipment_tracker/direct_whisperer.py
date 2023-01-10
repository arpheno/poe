import requests
from redislite import Redis

from poe.trade.headers import headers
from poe.trade.rate_limiter import limit_rate


class DirectWhisperer:
    def __init__(self, cache=Redis()):
        self.cache = cache
        self.url = 'https://www.pathofexile.com/api/trade/whisper'

    def direct_whisper(self, token):
        key = "trade-whisper-request-limit"
        limits = ['3:10:5', '15:60:60', '75:600:600', '150:3600:3600', '600:43200:3600']

        with limit_rate(key, limits, self.cache):
            response = requests.post(self.url,
                                     json=dict(token=token),
                                     headers={'x-requested-with': 'XMLHttpRequest', **headers})
        return response.json()
