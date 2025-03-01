from sqlalchemy import Column, TIMESTAMP, UUID, VARCHAR, func
import uuid
from .base import Base

class MLExecution(Base):
    __tablename__ = "ml_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(TIMESTAMP, nullable=False, default=func.now())
    version = Column(VARCHAR, nullable=False)
