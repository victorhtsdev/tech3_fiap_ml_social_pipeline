import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.content import Content
from sqlalchemy.orm import sessionmaker
from config.database import engine
import numpy as np
from models.content_processed import ContentProcessed

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def update_embeddings(session: Session, records, embeddings):
    try:
        for record, embedding in zip(records, embeddings):
            filters = {
                "exec_id": record.exec_id,
                "content_id": record.content_id,
                "processed_id": record.processed_id
            }

            if not isinstance(embedding, bytes):
                embedding = np.array(embedding, dtype=np.float32).tobytes()

            affected_rows = session.query(ContentProcessed).filter_by(**filters).update({"embeddings": embedding})

            if affected_rows == 0:
                logging.warning(f"No rows updated for exec_id: {record.exec_id}, content_id: {record.content_id}, processed_id: {record.processed_id}")

            else:
                logging.info(f"Updated embeddings for exec_id: {record.exec_id}, content_id: {record.content_id}, processed_id: {record.processed_id}")

        session.commit()
        logging.info(f"Successfully updated {len(records)} records in processed_content.")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error updating embeddings: {str(e)}")
        raise


def update_cluster_ids(records, labels):
    session = SessionLocal()
    try:
        for record, cluster_id in zip(records, labels):
            filters = {
                "exec_id": record["exec_id"],
                "content_id": record["content_id"],
                "processed_id": record["processed_id"]
            }

            cluster_id = int(cluster_id)

            affected_rows = (
                session.query(ContentProcessed)
                .filter_by(**filters)
                .update({"cluster_id": cluster_id})
            )

            if affected_rows == 0:
                logging.warning(f"No rows updated for exec_id: {record['exec_id']}, content_id: {record['content_id']}, processed_id: {record['processed_id']}")

        session.commit()
        logging.info(f"Successfully updated {len(records)} records in processed_content.")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error updating clusters: {str(e)}")
        raise

    except Exception as e:
        session.rollback()
        logging.error(f"Unexpected error updating clusters: {str(e)}")
        raise

    finally:
        session.close()

def update_processed_content(records):
    session = SessionLocal()
    try:
        for record in records:
            filters = {
                "id": record["id"],
                "source": record["source"],
                "user_id": record["user_id"],
                "user_id2": record["user_id2"],
                "date_posted": record["date_posted"]
            }

            affected_rows = (
                session.query(Content)
                .filter_by(**filters)
                .update({"content_processed": record["content_processed"]})
            )

            if affected_rows == 0:
                logging.warning(f"⚠️ No rows updated for ID: {record['id']}. Check primary key!")

        session.commit()
        logging.info(f"✅ Successfully updated {len(records)} records in content_processed.")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"❌ Error updating content_processed: {str(e)}")
        raise

    except Exception as e:
        session.rollback()
        logging.error(f"❌ Unexpected error updating content_processed: {str(e)}")
        raise

    finally:
        session.close()
