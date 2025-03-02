from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from config.database import engine
from models.ml_execution import MLExecution

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

import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config.database import engine
from models.content import Content

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config.database import engine
from models.content import Content

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
