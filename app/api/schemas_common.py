from typing import List
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


class GenericModelInfoResponse(BaseModel):
    company_type: str
    model_name: str
    target_name: str
    target_transform: str
    notes: List[str]