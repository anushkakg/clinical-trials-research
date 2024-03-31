from pydantic import BaseModel


class EnumData(BaseModel):
    piece: str
    field: str
    missingStudiesCount: int
    uniqueValuesCount: int
