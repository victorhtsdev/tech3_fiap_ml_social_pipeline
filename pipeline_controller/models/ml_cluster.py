from sqlalchemy import Column, String, TIMESTAMP, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base

class MLCluster(Base):
    __tablename__ = "ml_clusters"

    exec_id = Column(UUID(as_uuid=True), ForeignKey("ml_execution.id", ondelete="CASCADE"), primary_key=True)
    cluster = Column(Integer, primary_key=True)
    topic = Column(String, nullable=True)
    pattern_found = Column(String, nullable=True)
    keyword = Column(String, nullable=True)
    conclusion = Column(String, nullable=True)
    is_consistent = Column(Boolean, nullable=True)
    record_count = Column(Integer, nullable=False) 
    created_at = Column(TIMESTAMP, nullable=False, default="NOW()")
