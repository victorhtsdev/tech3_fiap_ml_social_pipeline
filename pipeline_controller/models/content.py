from sqlalchemy import Column, TIMESTAMP, UUID, VARCHAR, TEXT, BYTEA, INTEGER
import uuid
from .base import Base

class Content(Base):
    __tablename__ = "content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(TEXT, nullable=False)
    source = Column(VARCHAR, nullable=False)
    date_posted = Column(TIMESTAMP)
    cluster_id = Column(INTEGER)
    embeddings = Column(BYTEA)
    user_id = Column(VARCHAR)
