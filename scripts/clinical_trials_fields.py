import sqlite3

import httpx
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Field(Base):
    __tablename__ = "fields"
    field_name = Column("name", String, primary_key=True)
    field_type = Column("type", String)
    field_piece = Column("piece", String)
    missing_studies = Column("missingStudiesCount", Integer)
    unique_values = Column("uniqueValuesCount", Integer)

    def __init__(
        self,
        field_name: str,
        field_type: str,
        field_piece: str,
        missing_studies: int,
        unique_values: int,
    ) -> None:
        self.field_name = field_name
        self.field_type = field_type
        self.field_piece = field_piece
        self.missing_studies = missing_studies
        self.unique_values = unique_values

    def __repr__(self) -> str:
        return f"{self.field_name} {self.field_type} {self.missing_studies} {self.unique_values}"


class FieldResponse(BaseModel):
    type: str
    piece: str
    field: str
    missingStudiesCount: int
    uniqueValuesCount: int


engine = create_engine("sqlite:///clinicaltrials.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

response_json = httpx.get(
    "https://clinicaltrials.gov/api/v2/stats/field/values?fields=Phase"
).json()
response = FieldResponse(**response_json[0])
phase_field = Field(
    field_name=response.field,
    field_type=response.type,
    field_piece=response.piece,
    missing_studies=response.missingStudiesCount,
    unique_values=response.uniqueValuesCount,
)
session.add(phase_field)
session.commit()
