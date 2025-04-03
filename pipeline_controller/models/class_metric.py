from sqlalchemy import Column, UUID, TEXT, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClassMetric(Base):
    __tablename__ = "class_metric"

    model_id = Column(UUID(as_uuid=True), ForeignKey("ml_model.id", ondelete="CASCADE"), nullable=False)
    class_name = Column(TEXT, nullable=False)
    f1_score = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint("model_id", "class_name"),
    )
