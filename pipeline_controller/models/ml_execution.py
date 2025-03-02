from sqlalchemy import Column, String, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base
import uuid

class MLExecution(Base):
    __tablename__ = "ml_execution"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search = Column(String, nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    version = Column(Integer, nullable=False)
