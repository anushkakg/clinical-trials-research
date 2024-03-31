from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

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
