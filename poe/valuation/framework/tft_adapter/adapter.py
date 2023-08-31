from json import JSONDecodeError

import requests
from requests import RequestException

from poe.valuation.framework.tft_adapter.factory import TimestampedWholesalePricesFactory

raw_file_content_url_base = 'https://raw.githubusercontent.com/The-Forbidden-Trove/tft-data-prices/master/lsc/'
api_url = 'https://api.github.com/repos/The-Forbidden-Trove/tft-data-prices/contents/lsc'

class TftAdapter:
    def __init__(self, url=raw_file_content_url_base, file_parser_factory=TimestampedWholesalePricesFactory):
        self.url = url
        self.file_parser_factory = file_parser_factory

    def adapt(self, *args, **kwargs):  # backwards compatible interface preserving
        files = self._fetch_safely(api_url)
        file_urls = [raw_file_content_url_base + file['name'] for file in files]
        file_data = [self._fetch_safely(file_url) for file_url in file_urls]
        models = [self.file_parser_factory.create(file['name']).parse_obj(data) for file, data in zip(files, file_data)]
        valuations = [model.as_valuations() for model in models]
        return [valuation for sublist in valuations for valuation in sublist]

    def _fetch_safely(self, file_url):
        try:
            return requests.get(file_url).json()
        except RequestException as e:
            raise ConnectionError("Error connecting to API URL: %s" % api_url) from e
        except JSONDecodeError as e:
            raise ValueError("Error parsing JSON response") from e
