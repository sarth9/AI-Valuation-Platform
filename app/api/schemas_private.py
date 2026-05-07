from typing import List, Optional
from pydantic import BaseModel, Field


class PrivateValuationInput(BaseModel):
    sector: str = Field(..., min_length=1)
    industry: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)

    annual_revenue: float = Field(..., gt=0)
    ebitda: float
    net_income: float
    total_cash: float = Field(..., ge=0)
    total_debt: float = Field(..., ge=0)
    total_assets: float = Field(..., gt=0)
    total_liabilities: float = Field(..., ge=0)
    shareholders_equity: float
    gross_margin: float
    operating_margin: float
    net_margin: float
    revenue_growth: float
    employee_count: int = Field(..., gt=0)
    company_age_years: float = Field(..., gt=0)

    free_cash_flow: Optional[float] = 0.0
    operating_cash_flow: Optional[float] = 0.0
    capex: Optional[float] = 0.0
    customer_count: Optional[int] = 0
    recurring_revenue_ratio: Optional[float] = 0.0


class PrivatePredictionResponse(BaseModel):
    company_type: str
    estimated_enterprise_value: float
    estimated_enterprise_value_millions: float
    valuation_band: str
    currency: str
    model_used: str
    explanation_points: List[str]