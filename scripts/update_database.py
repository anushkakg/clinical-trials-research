from ctr.api import get_integer_fields
from ctr.tables import IntegerField
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

fields = get_integer_fields()

Base = declarative_base()
db = create_engine("sqlite:///clinicaltrials.db", echo=True)
Base.metadata.create_all(bind=db)
Session = sessionmaker(bind=db)

with Session() as session:
    for field in fields:
        entry = IntegerField(
            piece=field.piece,
            field=field.field,
            missing_studies_count=field.missingStudiesCount,
            min=field.min,
            max=field.max,
            avg=field.avg,
        )
        session.add(entry)
    session.commit()
