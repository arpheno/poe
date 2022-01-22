from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Pay(BaseModel):
    id: int
    league_id: int
    pay_currency_id: int
    get_currency_id: int
    sample_time_utc: str
    count: int
    value: float
    data_point_count: int
    includes_secondary: bool
    listing_count: int


class Receive(BaseModel):
    id: int
    league_id: int
    pay_currency_id: int
    get_currency_id: int
    sample_time_utc: str
    count: int
    value: float
    data_point_count: int
    includes_secondary: bool
    listing_count: int


class PaySparkLine(BaseModel):
    data: List[Optional[float]]
    totalChange: float


class ReceiveSparkLine(BaseModel):
    data: List[float]
    totalChange: float


class LowConfidencePaySparkLine(BaseModel):
    data: List[Optional[float]]
    totalChange: float


class LowConfidenceReceiveSparkLine(BaseModel):
    data: List[float]
    totalChange: float


class Line(BaseModel):
    currencyTypeName: str
    pay: Optional[Pay] = None
    receive: Receive
    paySparkLine: PaySparkLine
    receiveSparkLine: ReceiveSparkLine
    chaosEquivalent: float
    lowConfidencePaySparkLine: LowConfidencePaySparkLine
    lowConfidenceReceiveSparkLine: LowConfidenceReceiveSparkLine
    detailsId: str


class CurrencyDetail(BaseModel):
    id: int
    icon: str
    name: str
    tradeId: Optional[str] = None


class Language(BaseModel):
    name: str
    translations: Dict[str, Any]


class CurrencyReply(BaseModel):
    lines: List[Line]
    currencyDetails: List[CurrencyDetail]
    language: Language
