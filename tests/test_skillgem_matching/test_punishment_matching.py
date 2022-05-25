from unittest.mock import Mock

from poe.matchers import match_skillgem

candidates = [
    {
        "corrupted": True,
        "gemLevel": 21,
        "gemQuality": 23,
    },
    {
        "corrupted": True,
        "gemLevel": 21,
        "gemQuality": 20,
    },
    {
        "corrupted": True,
        "gemLevel": 20,
        "gemQuality": 23,
    },
    {
        "gemLevel": 20,
        "gemQuality": 20,
    },
    {
        "corrupted": True,
        "gemLevel": 20,
        "gemQuality": 20,
    },
    {
        "gemLevel": 1,
        "gemQuality": 20,
    },
    {
        "gemLevel": 20,
    },
    {
        "corrupted": True,
        "gemLevel": 21,
    },
    {
        "corrupted": True,
        "gemLevel": 20,
    },
    {
        "gemLevel": 1,
    },
]


def test_match_empower():
    item = Mock(level=18, quality=20, corrupted=False)
    assert match_skillgem(candidates, item) == candidates[5]
