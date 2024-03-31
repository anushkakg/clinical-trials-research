import httpx
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

API_URL = "https://clinicaltrials.gov/api/v2/stats/field/values?types=ENUM"
Base = declarative_base()


class EnumField(Base):
    __tablename__ = "enumfields"
    piece = Column("piece", String, primary_key=True)
    field = Column("field", String)
    missing_studies_count = Column("missingStudiesCount", Integer)
    unique_values_count = Column("uniqueValuesCount", Integer)

    def __init__(
        self,
        piece: str,
        field: str,
        missing_studies_count: str,
        unique_values_count: str,
    ) -> None:
        self.piece = piece
        self.field = field
        self.missing_studies_count = missing_studies_count
        self.unique_values_count = unique_values_count


class EnumData(BaseModel):
    piece: str
    field: str
    missingStudiesCount: int
    uniqueValuesCount: int


engine = create_engine("sqlite:///clinicaltrials.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

response_json = httpx.get(API_URL).json()
for i in response_json:
    data = EnumData(**i)
    field_entry = EnumField(
        piece=data.piece,
        field=data.field,
        missing_studies_count=data.missingStudiesCount,
        unique_values_count=data.uniqueValuesCount,
    )
    session.add(field_entry)
