from dataclasses import dataclass

import pendulum as pendulum

from valuation.framework.valuation import Valuation

influence = "influence"

gem_quality = "gem_quality"

gem_level = "gem_level"

ilvl = "item_level"


@dataclass
class MapToAdaptation:
    mapping: {str: str}

    def __call__(self, item):
        return {key: item.get(value, None) for key, value in self.mapping.items()}


ninja_hash_key_mappers = {
    "Map": MapToAdaptation({"name": "name", "map_tier": "mapTier"}),
    "ClusterJewel": MapToAdaptation(
        {"significant_enchant": "name", "passives": "variant", ilvl: "levelRequired"}
    ),
    "BaseType": MapToAdaptation(
        {ilvl: "levelRequired", influence: "variant", "base": "baseType"}
    ),
    "UniqueAccessory": MapToAdaptation(
        { "base": "baseType",'name':'name'}
    ),
    "SkillGem": MapToAdaptation(
        {
            gem_level: "gemLevel",
            gem_quality: "gemQuality",
            "name": "name",
            "corrupted": "corrupted",
        }
    ),
    "UniqueWeapon": MapToAdaptation({"name": "name", "links": "links"}),
    "UniqueArmour": MapToAdaptation({"name": "name", "links": "links"}),
    "UniqueMap": MapToAdaptation({"name": "name", "map_tier": "mapTier"}),
    "UniqueJewel": MapToAdaptation({ "base": "baseType",'name':'name','passives':'variant'})
}


class NinjaAdapter:
    def adapt(self, prices):
        timestamp = pendulum.now().int_timestamp
        valuations = []
        for key, values in prices.items():
            for value in values:
                if (
                    value["name"]
                    in ["Empower Support", "Enlighten Support", "Enhance Support"]
                    and value["gemLevel"] > 2
                ):
                    value["gemQuality"] = None
                if "-relic" in value.get("detailsId", ""):
                    continue
                hash_key = ninja_hash_key_mappers.get(
                    value["type"], MapToAdaptation({"name": "name"})
                )(value)
                valuations.append(
                    Valuation(
                        key=hash_key,
                        estimate=value["chaosValue"],
                        info="poe.ninja",
                        tags=['poe.ninja','purchasable'],
                        timestamp=timestamp,
                    )
                )

        return valuations
