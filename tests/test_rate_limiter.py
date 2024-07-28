import asyncio

import pytest

from proxy.rate_limit_parser import parse_rate_limit_headers, RateLimit, parse_for_timeout, check_rate_limit_violation
from proxy.ratelimitcounter import RatelimitCounter

@pytest.fixture
def counter():
    return RatelimitCounter()

@pytest.mark.asyncio
@pytest.mark.parametrize("rate_limit_period", [0.1, 0.2, 0.3])
async def test_increment(counter, rate_limit_period):
    counter.increment('test_key', rate_limit_period=rate_limit_period)
    assert counter['test_key'] == 1, "The counter should be incremented by 1"
    await asyncio.sleep(rate_limit_period-0.1)
    assert counter['test_key'] == 1, f"The counter should still be 1 after {rate_limit_period-0.1} seconds"
    await asyncio.sleep(rate_limit_period+0.1)
    assert counter['test_key'] == 0, f"The counter should be 0 after {rate_limit_period+0.1} seconds"


import pytest
from unittest.mock import patch, Mock


@pytest.fixture
def rate_limit_headers_with_limit():
    return {
        'X-Rate-Limit-Policy': 'Policy1',
        'X-Rate-Limit-Rules': 'Rule1',
        'X-Rate-Limit-Rule1': '100:60:3600',
        'X-Rate-Limit-Rule1-State': '50:60:3600'
    }


@pytest.fixture
def rate_limit_headers_without_limit():
    return {
        'X-Rate-Limit-Policy': 'policy1',
        'X-Rate-Limit-Rules': 'rule1',
    }


def test_parse_rate_limit_headers_with_limit(rate_limit_headers_with_limit):

    rate_limit_configs,state = parse_rate_limit_headers(rate_limit_headers_with_limit)

    assert len(rate_limit_configs) == 1
    assert rate_limit_configs[0] == RateLimit(policy='policy1', rule_type='Rule1', requests=100, period=60,
                                              duration=3600)


def test_parse_rate_limit_headers_without_limit(rate_limit_headers_without_limit):
    rate_limit_configs,state = parse_rate_limit_headers(rate_limit_headers_without_limit)

    assert len(rate_limit_configs) == 0


def test_parse_for_timeout():
    response = Mock()
    response.headers = {'content-type': 'application/json', 'content-length': '97',
                        'X-Rate-Limit-Policy': 'trade-search-request-limit', 'X-Rate-Limit-Rules': 'Account,Ip',
                        'X-Rate-Limit-Account': '3:5:60', 'X-Rate-Limit-Account-State': '1:5:0',
                        'X-Rate-Limit-Ip': '8:10:60,15:60:120,60:300:1800',
                        'X-Rate-Limit-Ip-State': '1:10:0,0:60:67,45:300:0'}
    assert parse_for_timeout(response) == 67
# Add other tests using the asyncio mark as needed...

def test_check_rate_limit_violation():
    response_headers = {'content-type': 'application/json', 'content-length': '97',
                        'X-Rate-Limit-Policy': 'trade-search-request-limit', 'X-Rate-Limit-Rules': 'Account,Ip',
                        'X-Rate-Limit-Account': '3:5:60', 'X-Rate-Limit-Account-State': '1:5:0',
                        'X-Rate-Limit-Ip': '8:10:60,15:60:120,60:300:1800',
                        'X-Rate-Limit-Ip-State': '1:10:0,0:60:67,45:300:0'}
    assert check_rate_limit_violation(response_headers) ==(RateLimit(policy='trade-search-request-limit', rule_type='Ip', requests=15, period=60, duration=120), 67)
if __name__ == '__main__':
    pytest.main()
