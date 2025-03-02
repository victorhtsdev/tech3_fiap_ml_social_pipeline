from sqlalchemy import Column, TIMESTAMP, UUID, VARCHAR, TEXT, func
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PipelineLog(Base):
    __tablename__ = "pipeline_log"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    timestamp = Column(TIMESTAMP, primary_key=True, nullable=False, default=func.now())
    stage = Column(VARCHAR, nullable=False)  
    status = Column(VARCHAR, nullable=False) 
    details = Column(TEXT)
