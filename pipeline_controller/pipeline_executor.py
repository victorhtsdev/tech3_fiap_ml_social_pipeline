import os
import logging
import openai
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models.content import Content
from config.database import engine
from data_storage.data_update import update_embeddings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
EMBEDDING_MODEL = "text-embedding-3-large"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def fetch_texts_for_embedding(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"Fetching text for exec_id: {exec_id}")

        texts = session.query(Content).filter(
            Content.embeddings.is_(None),
            Content.id == exec_id
        ).limit(1).all()

        if not texts:
            logging.info(f"No records found for exec_id: {exec_id}")
            return []

        for record in texts:
            logging.info(f"Original content: {record.content}")  # 🔹 Log do texto enviado para embedding

        return texts

    except SQLAlchemyError as e:
        logging.error(f"Database error while fetching texts: {str(e)}")
        raise

    finally:
        session.close()

def generate_embeddings(text_list):
    try:
        logging.info(f"Generating embeddings for {len(text_list)} text(s)")

        client = openai.OpenAI()
        response = client.embeddings.create(
            input=text_list,
            model=EMBEDDING_MODEL
        )

        embeddings = [np.array(item.embedding, dtype=np.float32).tobytes() for item in response.data]

        for text, embedding in zip(text_list, response.data):
            logging.info(f"🔹 Sent text: {text}")  # Log do texto enviado
            logging.info(f"🔹 Generated embedding (first 5 values): {embedding.embedding[:5]}")  # Mostra só os primeiros valores para não poluir

        logging.info(f"Generated {len(embeddings)} embedding(s) successfully.")
        return embeddings

    except Exception as e:
        logging.error(f"Error generating embeddings: {str(e)}")
        raise

def process_embeddings(exec_id):  
    session = SessionLocal()

    try:
        logging.info(f"Starting embedding process for exec_id: {exec_id}")

        records = fetch_texts_for_embedding(exec_id)

        if not records:
            logging.info(f"No records to process for exec_id: {exec_id}")
            return

        texts = [record.content for record in records]
        logging.info(f"Processing {len(texts)} text(s) for embedding.")

        embeddings = generate_embeddings(texts)

        if len(embeddings) == len(records):
            logging.info(f"Updating {len(records)} record(s) with embeddings in database.")

            update_embeddings(session, records, embeddings)
            session.commit()

            logging.info(f"✅ Successfully updated {len(records)} embeddings in database.")

        else:
            logging.error("Embedding count does not match text count.")
            raise ValueError("Embedding count mismatch.")

    except Exception as e:
        logging.error(f"Embedding processing error: {str(e)}")
        session.rollback()
        raise

    finally:
        session.close()
        logging.info("Embedding process completed.")
