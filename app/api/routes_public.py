from fastapi import APIRouter, HTTPException

from app.api.comparison_service import fetch_company_market_data
from app.api.predictor_public import public_model_service
from app.api.schemas_common import ErrorResponse, GenericModelInfoResponse
from app.api.schemas_public import (
    PublicComparisonResponse,
    PublicPredictionResponse,
    PublicValuationInput,
)


router = APIRouter(prefix="/public", tags=["Public Company Valuation"])


def payload_to_dict(payload: PublicValuationInput) -> dict:
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return payload.dict()


@router.get(
    "/model-info",
    response_model=GenericModelInfoResponse,
    responses={500: {"model": ErrorResponse}},
)
def get_public_model_info():
    return GenericModelInfoResponse(**public_model_service.get_model_info())


@router.post(
    "/predict",
    response_model=PublicPredictionResponse,
    responses={500: {"model": ErrorResponse}},
)
def predict_public_valuation(payload: PublicValuationInput):
    try:
        input_data = payload_to_dict(payload)
        prediction, explanation = public_model_service.predict_with_explanation(input_data)

        return PublicPredictionResponse(
            company_type="public_company",
            predicted_market_cap=prediction,
            predicted_market_cap_billions=round(prediction / 1_000_000_000, 2),
            currency="USD",
            model_used=public_model_service.model_name,
            explanation_points=explanation,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Public prediction failed: {str(exc)}")


@router.get(
    "/compare/{ticker}",
    response_model=PublicComparisonResponse,
    responses={500: {"model": ErrorResponse}},
)
def compare_public_company(ticker: str):
    try:
        ticker = ticker.strip().upper()
        if not ticker:
            raise HTTPException(status_code=400, detail="Ticker cannot be empty.")

        company_data = fetch_company_market_data(ticker)

        required_payload = {
            "sector": company_data.get("sector") or "Unknown",
            "industry": company_data.get("industry") or "Unknown",
            "enterprise_value": company_data.get("enterprise_value") or 0,
            "total_revenue": company_data.get("total_revenue") or 1,
            "ebitda": company_data.get("ebitda") or 0,
            "net_income": company_data.get("net_income") or 0,
            "total_cash": company_data.get("total_cash") or 0,
            "total_debt": company_data.get("total_debt") or 0,
            "book_value": company_data.get("book_value") or 0,
            "current_ratio": company_data.get("current_ratio") or 0,
            "debt_to_equity": company_data.get("debt_to_equity") or 0,
            "return_on_assets": company_data.get("return_on_assets") or 0,
            "return_on_equity": company_data.get("return_on_equity") or 0,
            "gross_margins": company_data.get("gross_margins") or 0,
            "operating_margins": company_data.get("operating_margins") or 0,
            "profit_margins": company_data.get("profit_margins") or 0,
            "revenue_growth": company_data.get("revenue_growth") or 0,
            "earnings_growth": company_data.get("earnings_growth") or 0,
            "trailing_pe": company_data.get("trailing_pe") or 0,
            "forward_pe": company_data.get("forward_pe") or 0,
            "price_to_book": company_data.get("price_to_book") or 0,
            "beta": company_data.get("beta") or 0,
            "shares_outstanding": company_data.get("shares_outstanding") or 1,
        }

        prediction = public_model_service.predict(required_payload)
        actual_market_cap = company_data.get("actual_market_cap")

        difference = None
        difference_billions = None
        comparison_status = "actual market cap unavailable"

        if actual_market_cap is not None:
            difference = prediction - actual_market_cap
            difference_billions = round(difference / 1_000_000_000, 2)

            if difference > 0:
                comparison_status = "model prediction is higher than actual market cap"
            elif difference < 0:
                comparison_status = "model prediction is lower than actual market cap"
            else:
                comparison_status = "model prediction matches actual market cap"

        return PublicComparisonResponse(
            ticker=company_data.get("ticker", ticker),
            company_name=company_data.get("company_name"),
            actual_market_cap=actual_market_cap,
            actual_market_cap_billions=round(actual_market_cap / 1_000_000_000, 2)
            if actual_market_cap is not None
            else None,
            predicted_market_cap=prediction,
            predicted_market_cap_billions=round(prediction / 1_000_000_000, 2),
            difference=difference,
            difference_billions=difference_billions,
            comparison_status=comparison_status,
        )

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Public comparison failed: {str(exc)}")