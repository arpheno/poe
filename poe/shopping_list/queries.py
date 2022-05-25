q = {
    "to_dust_20": {
        "query": {
            "status": {"option": "online"},
            "name": "To Dust",
            "type": "Cobalt Jewel",
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {
                            "id": "explicit.stat_1331384105",
                            "disabled": False,
                            "value": {"max": -20},
                        }
                    ],
                    "disabled": False,
                }
            ],
        }
    },
    "to_dust_19": {
        "query": {
            "status": {"option": "online"},
            "name": "To Dust",
            "type": "Cobalt Jewel",
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {
                            "id": "explicit.stat_1331384105",
                            "disabled": False,
                            "value": {
                                "max": -19,
                                "min": -19,
                            },
                        }
                    ],
                    "disabled": False,
                }
            ],
        }
    },
    "stygian": {
        "query": {
            "status": {"option": "any"},
            "type": "Stygian Vise",
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {
                            "id": "explicit.stat_644456512",
                            "value": {"min": 15},
                            "disabled": False,
                        },
                        {
                            "id": "pseudo.pseudo_total_life",
                            "value": {"min": 90},
                            "disabled": False,
                        },
                    ],
                },
                {
                    "filters": [
                        {
                            "id": "pseudo.pseudo_number_of_crafted_suffix_mods",
                            "value": {"min": 1},
                            "disabled": False,
                        },
                        {
                            "id": "pseudo.pseudo_number_of_suffix_mods",
                            "value": {"max": 2},
                            "disabled": False,
                        },
                    ],
                    "type": "count",
                    "value": {"min": 1},
                },
            ],
        },
        "sort": {"price": "asc"},
    },
    "abyss": {
        "query": {
            "status": {"option": "online"},
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {
                            "id": "pseudo.pseudo_total_elemental_resistance",
                            "value": {"min": 35},
                            "disabled": False,
                        }
                    ],
                }
            ],
            "filters": {
                "type_filters": {"filters": {"category": {"option": "jewel.abyss"}}}
            },
        },
        "sort": {"price": "asc"},
    },
    "olroths": {
        "query": {
            "status": {"option": "any"},
            "name": "Olroth's Resolve",
            "type": "Iron Flask",
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {
                            "id": "explicit.stat_388617051",
                            "value": {"max": 40},
                            "disabled": False,
                        }
                    ],
                }
            ],
        },
        "sort": {"price": "asc"},
    },
    "amulet": {
        "query": {
            "status": {"option": "any"},
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {"id": "pseudo.pseudo_total_life", "disabled": False},
                        {
                            "id": "pseudo.pseudo_total_elemental_resistance",
                            "disabled": False,
                        },
                        {"id": "explicit.stat_493812998", "disabled": False},
                    ],
                    "disabled": False,
                }
            ],
            "filters": {
                "type_filters": {
                    "filters": {"category": {"option": "accessory.amulet"}},
                    "disabled": False,
                }
            },
        },
        "sort": {"price": "asc"},
    },
    "timeless": {
        "query": {
            "status": {"option": "online"},
            "name": "Brutal Restraint",
            "type": "Timeless Jewel",
            "stats": [
                {"type": "and", "filters": []},
                {
                    "filters": [
                        {
                            "id": "explicit.pseudo_timeless_jewel_balbala",
                            "value": {"min": 6015, "max": 6015},
                            "disabled": False,
                        },
                        {
                            "id": "explicit.pseudo_timeless_jewel_balbala",
                            "value": {"min": 1000, "max": 2000},
                            "disabled": False,
                        },
                    ],
                    "type": "count",
                    "value": {"min": 1},
                },
            ],
        },
        "sort": {"price": "asc"},
    },
    "skeletons": {
        "query": {
            "status": {"option": "online"},
            "type": "Summon Skeletons",
            "stats": [{"type": "and", "filters": [], "disabled": False}],
            "filters": {
                "misc_filters": {
                    "filters": {"gem_alternate_quality": {"option": "1"}},
                    "disabled": False,
                }
            },
        },
        "sort": {"price": "asc"},
    },
    "secrets_of_suffering": {
        "query": {
            "status": {"option": "online"},
            "name": "The Interrogation",
            "type": "Small Cluster Jewel",
            "stats": [{"type": "and", "filters": []}],
        },
        "sort": {"price": "asc"},
    },
    "minion_speed": {
        "query": {
            "status": {"option": "online"},
            "type": "Minion Speed Support",
            "stats": [{"type": "and", "filters": []}],
            "filters": {
                "misc_filters": {"filters": {"gem_alternate_quality": {"option": "1"}}}
            },
        },
        "sort": {"price": "asc"},
    },
}
