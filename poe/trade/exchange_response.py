from __future__ import annotations

from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field


class Online(BaseModel):
    league: str
    status: Optional[str] = None


class Account(BaseModel):
    name: str
    last_character_name: str = Field(..., alias='lastCharacterName')
    online: Union[Online,bool]
    language: str


class Exchange(BaseModel):
    currency: str
    amount: float
    whisper: str


class Item(BaseModel):
    currency: str
    amount: int
    stock: int
    id: str
    whisper: str


class Offer(BaseModel):
    exchange: Exchange
    item: Item


class Listing(BaseModel):
    indexed: str
    account: Account
    offers: List[Offer]
    whisper: str


class ResultItem(BaseModel):
    id: str
    item: Any
    listing: Listing


class ExchangeResponse(BaseModel):
    id: str
    complexity: Any
    result: List[ResultItem]
    total: int
