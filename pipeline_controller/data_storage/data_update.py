import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.content import Content
import numpy as np

def update_embeddings(session: Session, records, embeddings):
    try:
        for record, embedding in zip(records, embeddings):
            filters = {
                "id": record.id,
                "source": record.source,
                "user_id": record.user_id,
                "user_id2": record.user_id2,
                "date_posted": record.date_posted
            }

            # 🔹 Garante que os embeddings sejam armazenados corretamente como BYTEA
            if not isinstance(embedding, bytes):
                embedding = np.array(embedding, dtype=np.float32).tobytes()

            affected_rows = session.query(Content).filter_by(**filters).update({"embeddings": embedding})

            if affected_rows == 0:
                logging.warning(f"⚠️ No rows updated for ID: {record.id}. Possible primary key issue!")

            else:
                logging.info(f"✅ Updated embeddings for ID: {record.id}")

        session.commit()
        logging.info(f"✅ Successfully updated {len(records)} records in database.")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"❌ Error updating embeddings: {str(e)}")
        raise
