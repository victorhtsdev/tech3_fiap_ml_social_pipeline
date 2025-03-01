from sqlalchemy import Column, TIMESTAMP, UUID, VARCHAR, TEXT, func
import uuid
from .base import Base

class PipelineLog(Base):
    __tablename__ = "pipeline_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(TIMESTAMP, nullable=False, default=func.now())
    stage = Column(VARCHAR, nullable=False)  
    status = Column(VARCHAR, nullable=False) 
    details = Column(TEXT) 
