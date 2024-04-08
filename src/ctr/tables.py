from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class FieldMixin:
    piece: Mapped[str] = mapped_column(primary_key=True)
    field: Mapped[str]
    missing_studies_count: Mapped[int]


class IntegerField(FieldMixin, Base):
    __tablename__ = "integerfields"
    min: Mapped[int]
    max: Mapped[int]
    avg: Mapped[float]
