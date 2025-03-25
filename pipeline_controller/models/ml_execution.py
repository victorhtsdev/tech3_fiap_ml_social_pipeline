from sqlalchemy import Column, String, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from config.database import Base
import uuid

class MLExecution(Base):
    __tablename__ = "ml_execution"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search = Column(String, nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    classification_model_version = Column(Integer, nullable=True) 
    classification_model_name = Column(String, nullable=True)  
    classification_model_type = Column(String, nullable=True)  
    date_ranges = Column(JSONB, nullable=True) 