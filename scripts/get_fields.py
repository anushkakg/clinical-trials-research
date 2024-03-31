import httpx
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ctr.endpoints import ENUM_FIELDS
from ctr.models import EnumData
from ctr.tables import EnumField

Base = declarative_base()

engine = create_engine("sqlite:///clinicaltrials.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

response_json = httpx.get(ENUM_FIELDS).json()
for i in response_json:
    data = EnumData(**i)
    field_entry = EnumField(
        piece=data.piece,
        field=data.field,
        missing_studies_count=data.missingStudiesCount,
        unique_values_count=data.uniqueValuesCount,
    )
    session.add(field_entry)

session.commit()
