from fastapi import APIRouter, HTTPException

from app.api.predictor_startup import startup_model_service
from app.api.schemas_common import ErrorResponse, GenericModelInfoResponse
from app.api.schemas_startup import (
    StartupPredictionResponse,
    StartupValuationInput,
)


router = APIRouter(prefix="/startup", tags=["Startup / SaaS Valuation"])


def payload_to_dict(payload: StartupValuationInput) -> dict:
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return payload.dict()


@router.get(
    "/model-info",
    response_model=GenericModelInfoResponse,
    responses={500: {"model": ErrorResponse}},
)
def get_startup_model_info():
    return GenericModelInfoResponse(**startup_model_service.get_model_info())


@router.post(
    "/predict",
    response_model=StartupPredictionResponse,
    responses={500: {"model": ErrorResponse}},
)
def predict_startup_valuation(payload: StartupValuationInput):
    try:
        input_data = payload_to_dict(payload)
        prediction = startup_model_service.predict(input_data)
        explanation = startup_model_service.generate_explanation(input_data)
        band = startup_model_service.get_band(prediction)

        return StartupPredictionResponse(
            company_type="startup_saas",
            estimated_valuation=prediction,
            estimated_valuation_millions=round(prediction / 1_000_000, 2),
            valuation_band=band,
            currency="USD",
            model_used=startup_model_service.model_name,
            explanation_points=explanation,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Startup prediction failed: {str(exc)}")