from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from config.database import engine
from models.ml_execution import MLExecution
from models.content_processed import ContentProcessed
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
        logging.info(f"Fetching all sentences for exec_id: {exec_id}")

        sentences = session.query(ContentProcessed).filter(
            (ContentProcessed.embeddings.is_(None)) | (ContentProcessed.embeddings == b''),
            ContentProcessed.exec_id == exec_id
        ).all()

        if not sentences:
            logging.info(f"No records found for exec_id: {exec_id}")
            return []

        return sentences

    except SQLAlchemyError as e:
        logging.error(f"Database error: {str(e)}")
        raise

    finally:
        session.close()

def get_content_data(exec_id):

    session = SessionLocal()
    try:
        logging.info(f"🔍 Fetching content for exec_id: {exec_id}")

        content_records = session.query(
            Content.exec_id,
            Content.content_id,
            Content.content,
            Content.source,
            Content.url,
            Content.user_id,
            Content.user_id2,
            Content.date_posted
        ).filter(Content.exec_id == exec_id).all()

        if not content_records:
            logging.warning(f"⚠️ No records found for exec_id: {exec_id}")
            return []

        return [
            {
                "exec_id": record.exec_id,
                "content_id": record.content_id,
                "content": record.content,
                "source": record.source,
                "url": record.url,
                "user_id": record.user_id,
                "user_id2": record.user_id2,
                "date_posted": record.date_posted,
            }
            for record in content_records
        ]
    
    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_content_data: {str(e)}")
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

def get_content_processed_data(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"Fetching processed content for exec_id: {exec_id}")

        processed_records = session.query(
            ContentProcessed.exec_id,
            ContentProcessed.content_id,
            ContentProcessed.processed_id,
            ContentProcessed.sentence,
            ContentProcessed.embeddings,
            ContentProcessed.cluster_id
        ).filter(ContentProcessed.exec_id == exec_id).all()

        if not processed_records:
            logging.warning(f"No records found for exec_id: {exec_id}")
            return []

        return [
            {
                "exec_id": record.exec_id,
                "content_id": record.content_id,
                "processed_id": record.processed_id,
                "sentence": record.sentence,
                "embeddings": record.embeddings,
                "cluster_id": record.cluster_id
            }
            for record in processed_records
        ]

    except SQLAlchemyError as e:
        logging.error(f"Database error in get_content_processed_data: {str(e)}")
        raise RuntimeError(f"Error in get_content_processed_data: {str(e)}")

    finally:
        session.close()
