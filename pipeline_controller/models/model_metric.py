from sqlalchemy import Column, UUID, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModelMetric(Base):
    __tablename__ = "model_metric"

    model_id = Column(UUID(as_uuid=True), ForeignKey("ml_model.id", ondelete="CASCADE"), primary_key=True)
    accuracy = Column(Float)
    macro_f1 = Column(Float)
    weighted_f1 = Column(Float)
