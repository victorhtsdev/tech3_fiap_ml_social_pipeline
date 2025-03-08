from sqlalchemy import Column, TIMESTAMP, UUID, VARCHAR, TEXT, Integer, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ContentProcessed(Base):
    __tablename__ = "content_processed"

    exec_id = Column(UUID(as_uuid=True), nullable=False)  
    content_id = Column(Integer, nullable=False) 
    processed_id = Column(Integer, nullable=False) 
    sentence = Column(TEXT, nullable=True)
    embeddings = Column(BYTEA, nullable=True)
    cluster_id = Column(Integer, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint("exec_id", "content_id", "processed_id"),  
    )
