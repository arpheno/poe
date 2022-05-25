def query_timeless_jewel(name_of, seed):
    data = {
        "query": {
            "status": {"option": "online"},
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {
                            "id": f"explicit.pseudo_timeless_jewel_{name_of}",
                            "value": {"min": seed, "max": seed},
                            "disabled": False,
                        }
                    ],
                }
            ],
        },
        "sort": {"price": "asc"},
    }
    return data
