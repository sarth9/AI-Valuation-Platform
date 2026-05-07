from fastapi import APIRouter, HTTPException

from app.api.predictor_private import private_model_service
from app.api.schemas_common import ErrorResponse, GenericModelInfoResponse
from app.api.schemas_private import (
    PrivatePredictionResponse,
    PrivateValuationInput,
)


router = APIRouter(prefix="/private", tags=["Private Company Valuation"])


def payload_to_dict(payload: PrivateValuationInput) -> dict:
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return payload.dict()


@router.get(
    "/model-info",
    response_model=GenericModelInfoResponse,
    responses={500: {"model": ErrorResponse}},
)
def get_private_model_info():
    return GenericModelInfoResponse(**private_model_service.get_model_info())


@router.post(
    "/predict",
    response_model=PrivatePredictionResponse,
    responses={500: {"model": ErrorResponse}},
)
def predict_private_valuation(payload: PrivateValuationInput):
    try:
        input_data = payload_to_dict(payload)
        prediction = private_model_service.predict(input_data)
        explanation = private_model_service.generate_explanation(input_data)
        band = private_model_service.get_band(prediction)

        return PrivatePredictionResponse(
            company_type="private_company",
            estimated_enterprise_value=prediction,
            estimated_enterprise_value_millions=round(prediction / 1_000_000, 2),
            valuation_band=band,
            currency="USD",
            model_used=private_model_service.model_name,
            explanation_points=explanation,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Private prediction failed: {str(exc)}")