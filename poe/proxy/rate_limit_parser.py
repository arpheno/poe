from dataclasses import dataclass
import datetime

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

    for rule in rules:
        rule_key = rule.strip().replace(' ', '-')
        limit_key = f'X-Rate-Limit-{rule_key}'
        state_key = f'X-Rate-Limit-{rule_key}-State'

        if limit_key in headers:
            rate_limits = parse_rate_limits(headers[limit_key])
            for limit in rate_limits:
                config = RateLimit(policy, rule_key, limit['requests'], limit['period'], limit['duration'])
                rate_limit_configs.append(config)

    return rate_limit_configs

def parse_rate_limits(rate_limit_str):
    return [parse_single_limit(limit) for limit in rate_limit_str.split(',')]

def parse_single_limit(limit_str):
    parts = limit_str.split(':')
    return {
        'requests': int(parts[0]),
        'period': int(parts[1]),
        'duration': int(parts[2])
    }