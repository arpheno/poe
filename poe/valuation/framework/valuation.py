from dataclasses import dataclass

def domain_hash_key(key:dict):
    return str(sorted(key.items()))
@dataclass
class Valuation:
    key: dict
    estimate: float
    timestamp: int
    tags:list
    info: str = ""

    def details(self):
        print(self.info)
        return self.info

    @property
    def hash_key(self):
        return domain_hash_key(self.key)
