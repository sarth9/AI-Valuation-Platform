from typing import List, Optional
from pydantic import BaseModel, Field


class StartupValuationInput(BaseModel):
    sector: str = Field(..., min_length=1)
    business_model: str = Field(..., min_length=1)
    funding_stage: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)

    arr: float = Field(..., ge=0)
    mrr: float = Field(..., ge=0)
    revenue_growth: float
    gross_margin: float
    burn_rate_monthly: float = Field(..., ge=0)
    runway_months: float = Field(..., ge=0)
    customer_count: int = Field(..., ge=0)
    churn_rate: float = Field(..., ge=0)
    net_revenue_retention: float = Field(..., ge=0)
    employee_count: int = Field(..., gt=0)

    cac: Optional[float] = 0.0
    ltv: Optional[float] = 0.0
    logo_retention: Optional[float] = 0.0
    active_users: Optional[int] = 0
    arpu: Optional[float] = 0.0


class StartupPredictionResponse(BaseModel):
    company_type: str
    estimated_valuation: float
    estimated_valuation_millions: float
    valuation_band: str
    currency: str
    model_used: str
    explanation_points: List[str]