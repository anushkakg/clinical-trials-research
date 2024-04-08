import httpx
from pydantic import BaseModel

FIELD_VALUES = "https://clinicaltrials.gov/api/v2/stats/field/values?types="
GET_INTEGER_FIELDS = FIELD_VALUES + "INTEGER"


class FieldValueResponse(BaseModel):
    piece: str
    field: str
    missingStudiesCount: int


class IntegerDataResponse(FieldValueResponse):
    min: int
    max: int
    avg: float


def get_integer_fields() -> list[IntegerDataResponse]:
    fields = []
    response_json = httpx.get(GET_INTEGER_FIELDS).json()
    for field in response_json:
        fields.append(IntegerDataResponse.model_validate(field))
    return fields
