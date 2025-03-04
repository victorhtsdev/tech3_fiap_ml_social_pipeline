from sqlalchemy import Column, TIMESTAMP, UUID, VARCHAR, TEXT, Integer, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import BYTEA
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Content(Base):
    __tablename__ = "content"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    content = Column(TEXT, nullable=False)
    content_processed = Column(TEXT, nullable=True)  
    source = Column(VARCHAR, nullable=False)
    url = Column(VARCHAR)
    user_id = Column(VARCHAR, nullable=False)
    user_id2 = Column(VARCHAR, nullable=False)
    date_posted = Column(TIMESTAMP, nullable=False)
    cluster_id = Column(Integer)
    embeddings = Column(BYTEA)

    __table_args__ = (
        PrimaryKeyConstraint("id", "source", "user_id", "user_id2", "date_posted"),  
    )
