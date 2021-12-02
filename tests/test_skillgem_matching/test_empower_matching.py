from unittest.mock import Mock

from item import SkillGem
from matchers.skillgem_matcher import match_skillgem

candidates = [
        {
            "name": "Empower Support",
            "corrupted": True,
            "gemLevel": 4,
            "chaosValue": 209.51,
            "detailsId": "empower-support-4c",
        },
        {
            "name": "Empower Support",
            "gemLevel": 3,
            "chaosValue": 34.0,
            "detailsId": "empower-support-3",
        },
        {
            "name": "Empower Support",
            "corrupted": True,
            "gemLevel": 3,
            "chaosValue": 17.0,
            "detailsId": "empower-support-3c",
        },
        {
            "name": "Empower Support",
            "gemLevel": 2,
            "chaosValue": 5.0,
            "detailsId": "empower-support-2",
        },
        {
            "name": "Empower Support",
            "corrupted": True,
            "gemLevel": 2,
            "gemQuality": 20,
            "chaosValue": 4.0,
            "detailsId": "empower-support-2c",
        },
        {
            "name": "Empower Support",
            "gemLevel": 1,
            "chaosValue": 3.0,
            "detailsId": "empower-support-1",
        },
        {
            "name": "Empower Support",
            "corrupted": True,
            "gemLevel": 1,
            "chaosValue": 3.0,
            "detailsId": "empower-support-1c",
        },
    ]

def test_match_empower():
    item = Mock(level=4,quality=23,corrupted=True)
    assert match_skillgem(candidates,item)['detailsId']== 'empower-support-4c'
