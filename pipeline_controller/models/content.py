from sqlalchemy import Column, TIMESTAMP, VARCHAR, TEXT, Integer, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Content(Base):
    __tablename__ = "content"

    exec_id = Column(UUID(as_uuid=True), nullable=False)  
    content_id = Column(Integer, nullable=False) 
    content = Column(TEXT, nullable=False)
    source = Column(VARCHAR, nullable=False)
    url = Column(VARCHAR)
    user_id = Column(VARCHAR, nullable=False)
    user_id2 = Column(VARCHAR, nullable=False)
    date_posted = Column(TIMESTAMP, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("exec_id", "content_id"),
    )
