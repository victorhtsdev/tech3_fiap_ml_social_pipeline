from sqlalchemy import Column, UUID, VARCHAR, TEXT, Integer, Boolean, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MLModel(Base):
    __tablename__ = "ml_model"

    id = Column(UUID(as_uuid=True), nullable=False)
    model_version = Column(Integer, nullable=True)
    model_name = Column(VARCHAR, nullable=True)
    model_type = Column(VARCHAR, nullable=True)
    model_path = Column(TEXT, nullable=True)
    is_recommended = Column(Boolean, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        UniqueConstraint("model_version", "model_name", "model_type", name="uq_model_name_type")
    )
