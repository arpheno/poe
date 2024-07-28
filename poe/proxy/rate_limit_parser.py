import datetime
from unittest.mock import Mock


@dataclass(frozen=True)
class RateLimit:
    policy: str
    rule_type: str
    requests: int
    period: int
    duration: int


def parse_rate_limit_headers(headers):
    policy = headers.get('X-Rate-Limit-Policy', '').replace(' ', '-').lower()
    rules = headers.get('X-Rate-Limit-Rules', '').split(',')
    rate_limit_configs = []
    states = {}
    for rule in rules:
        rule_key = rule.strip().replace(' ', '-')
        limit_key = f'X-Rate-Limit-{rule_key}'
        state_key = f'X-Rate-Limit-{rule_key}-State'

        if limit_key in headers:
            rate_limits = parse_rate_limits(headers[limit_key])
            for limit in rate_limits:
                config = RateLimit(policy, rule_key, limit['requests'], limit['period'], limit['duration'])
                rate_limit_configs.append(config)
        if limit_key in headers:
            rate_limits = parse_rate_limits(headers[limit_key])
            rate_states = parse_rate_limits(headers[state_key])
            for state in rate_states:
                config = RateLimit(policy, rule_key, limit['requests'], limit['period'], limit['duration'])
                states[config] = state['requests']
    return rate_limit_configs, states


def parse_rate_limits(rate_limit_str):
    return [parse_single_limit(limit) for limit in rate_limit_str.split(',')]


def parse_single_limit(limit_str):
    parts = limit_str.split(':')
    return {
        'requests': int(parts[0]),
        'period': int(parts[1]),
        'duration': int(parts[2])
    }




# implement parse for timeout
def parse_for_timeout(response):
    policy = response.headers.get('X-Rate-Limit-Policy', '').replace(' ', '-').lower()
    for key, value in response.headers.items():
        if key.endswith('State'):
            limits = parse_rate_limits(value)
            for limit in limits:
                if limit['duration'] >0:
                    rule = key.split('-')[-2]
                    policy = RateLimit(policy=policy, rule_type=rule, requests=limit['requests'], period=limit['period'], duration=limit['duration'])
                    return limit['duration']


import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimit:
    policy: str
    rule_type: str
    requests: int
    period: int
    duration: int


def parse_limit(header_value):
    """Parse the X-Rate-Limit-* header values into a list of tuples."""
    return [tuple(map(int, rule.split(':'))) for rule in header_value.split(',')]


def parse_state(header_value):
    """Parse the X-Rate-Limit-*-State header values into a list of tuples."""
    return [tuple(map(int, state.split(':'))) for state in header_value.split(',')]


def check_rate_limit_violation(response_headers)->(RateLimit, int):
    limits = {
        'Account': parse_limit(response_headers.get('X-Rate-Limit-Account', '')),
        'Ip': parse_limit(response_headers.get('X-Rate-Limit-Ip', ''))
    }

    states = {
        'Account': parse_state(response_headers.get('X-Rate-Limit-Account-State', '')),
        'Ip': parse_state(response_headers.get('X-Rate-Limit-Ip-State', ''))
    }

    for rule_type, limit_info in limits.items():
        for i, (requests, period, duration) in enumerate(limit_info):
            remaining, reset_after, penalty_time = states[rule_type][i]
            if penalty_time > 0:
                rate_limit = RateLimit(policy=response_headers['X-Rate-Limit-Policy'],
                                       rule_type=rule_type,
                                       requests=requests,
                                       period=period,
                                       duration=duration)
                return rate_limit, penalty_time

    return None, None

