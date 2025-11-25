from typing import Optional, List, Union, Literal
from pydantic import BaseModel, Field

class ItemQuery(BaseModel):
    name: Optional[str] = None
    baseType: Optional[str] = None
    type: Optional[str] = None
    gem_level: Optional[int] = Field(None, alias="gemLevel")
    gem_quality: Optional[int] = Field(None, alias="gemQuality")
    corrupted: Optional[bool] = None
    links: Optional[int] = None
    discriminator: Optional[str] = None # For things like "variant" in ninja
    
    class Config:
        frozen = True # Make it hashable so it can be used as a cache key

    def matches(self, item: dict) -> bool:
        """
        Check if a raw item dict matches this query.
        """
        if self.name and self.name != item.get("name"):
            return False
        if self.baseType and self.baseType != item.get("baseType"):
            return False
        if self.type and self.type != item.get("type"):
            return False
        if self.gem_level is not None and self.gem_level != item.get("gemLevel"):
            return False
        if self.gem_quality is not None and self.gem_quality != item.get("gemQuality"):
            return False
        if self.corrupted is not None and self.corrupted != item.get("corrupted"):
            return False
        if self.links is not None and self.links != item.get("links"):
            return False
        return True

class Ingredient(BaseModel):
    query: ItemQuery
    quantity: int = 1
    
    class Config:
        frozen = True
