from typing import List, Optional
from pydantic import BaseModel, Field


class PublicValuationInput(BaseModel):
    sector: str = Field(..., min_length=1)
    industry: str = Field(..., min_length=1)

    total_revenue: float = Field(..., gt=0)
    ebitda: float
    net_income: float
    total_cash: float = Field(..., ge=0)
    total_debt: float = Field(..., ge=0)
    current_ratio: float = Field(..., ge=0)
    debt_to_equity: float = Field(..., ge=0)
    gross_margins: float
    operating_margins: float
    profit_margins: float
    revenue_growth: float
    earnings_growth: float
    shares_outstanding: float = Field(..., gt=0)

    return_on_assets: Optional[float] = 0.0
    return_on_equity: Optional[float] = 0.0
    trailing_pe: Optional[float] = 0.0
    forward_pe: Optional[float] = 0.0
    price_to_book: Optional[float] = 0.0
    beta: Optional[float] = 0.0

    enterprise_value: Optional[float] = 0.0
    book_value: Optional[float] = 0.0


class PublicPredictionResponse(BaseModel):
    company_type: str
    predicted_market_cap: float
    predicted_market_cap_billions: float
    currency: str
    model_used: str
    explanation_points: List[str]


class PublicComparisonResponse(BaseModel):
    ticker: str
    company_name: Optional[str] = None
    actual_market_cap: Optional[float] = None
    actual_market_cap_billions: Optional[float] = None
    predicted_market_cap: float
    predicted_market_cap_billions: float
    difference: Optional[float] = None
    difference_billions: Optional[float] = None
    comparison_status: str