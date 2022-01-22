
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Sparkline(BaseModel):
    data: List[Optional[float]]
    totalChange: float


class LowConfidenceSparkline(BaseModel):
    data: List[Optional[float]]
    totalChange: float


class ImplicitModifier(BaseModel):
    text: str
    optional: bool


class ExplicitModifier(BaseModel):
    text: str
    optional: bool


class ModelItem(BaseModel):
    id: int
    name: str
    icon: str
    stackSize: Optional[int] = None
    itemClass: int
    sparkline: Sparkline
    lowConfidenceSparkline: LowConfidenceSparkline
    implicitModifiers: List[ImplicitModifier]
    explicitModifiers: List[ExplicitModifier]
    flavourText: str
    chaosValue: float
    exaltedValue: float
    count: int
    detailsId: str
    listingCount: Optional[int] = None
    baseType: Optional[str] = None
    mapTier: Optional[int] = None
    mapRegion: Optional[str] = None
    itemType: Optional[str] = None
    variant: Optional[str] = None
    levelRequired: Optional[int] = None
    links: Optional[int] = None
    artFilename: Optional[str] = None
    corrupted: Optional[bool] = None
    gemLevel: Optional[int] = None
    gemQuality: Optional[int] = None


class Model(BaseModel):
    __root__: List[ModelItem]