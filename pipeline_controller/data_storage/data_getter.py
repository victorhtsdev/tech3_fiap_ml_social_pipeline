from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from config.database import engine
from models.ml_execution import MLExecution
from models.content import Content
import logging

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_latest_version(search):
    session = SessionLocal()
    try:
        latest_execution = session.query(MLExecution.version)\
            .filter(MLExecution.search == search)\
            .order_by(desc(MLExecution.version))\
            .first()
        
        return latest_execution.version if latest_execution else 0

    except SQLAlchemyError as e:
        session.rollback()
        return 0  

    finally:
        session.close()

def get_texts_for_embedding(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"Fetching all texts for exec_id: {exec_id}")

        texts = session.query(Content).filter(
            (Content.embeddings.is_(None)) | (Content.embeddings == b''),
            Content.id == exec_id
        ).all()

        if not texts:
            logging.info(f"No records found for exec_id: {exec_id}")
            return []

        return texts

    except SQLAlchemyError as e:
        logging.error(f"Database error: {str(e)}")
        raise

    finally:
        session.close()

def get_content_data(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"Fetching content and embeddings for exec_id: {exec_id}")

        content_records = session.query(
            Content.id,
            Content.content,
            Content.embeddings,
            Content.date_posted,
            Content.source,
            Content.user_id,
            Content.user_id2
        ).filter(Content.id == exec_id).all()

        if not content_records:
            logging.warning(f"No records found for exec_id: {exec_id}")
            return []

        return [
            {
                "id": record.id,
                "content": record.content,
                "embeddings": record.embeddings,
                "source": record.source,
                "user_id": record.user_id,
                "user_id2": record.user_id2,
                "date_posted": record.date_posted,
            }
            for record in content_records
        ]
    
    except SQLAlchemyError as e:
        logging.error(f"Database error in get_content_data: {str(e)}")
        raise RuntimeError(f"Error in get_content_data: {str(e)}")

    finally:
        session.close()


def get_ml_execution_data(exec_id: str):
    session = SessionLocal()
    try:
        logging.info(f"Fetching ML execution data for exec_id: {exec_id}")

        result = session.query(MLExecution).filter(MLExecution.id == exec_id).first()

        if not result:
            logging.warning(f"No execution data found for exec_id: {exec_id}")
            return None

        return {
            "id": str(result.id),
            "search": result.search,
            "date": result.date,
            "version": result.version
        }

    except SQLAlchemyError as e:
        logging.error(f"Database error in get_ml_execution_data: {str(e)}")
        raise RuntimeError(f"Error in get_ml_execution_data: {str(e)}")

    finally:
        session.close()