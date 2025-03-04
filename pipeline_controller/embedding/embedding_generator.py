import os
import logging
import openai
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models.content import Content
from config.database import engine
from data_storage.data_update import update_embeddings
from data_storage.data_getter import get_texts_for_embedding

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", 1))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def generate_embeddings(text_list):
    try:
        logging.info(f"Generating embeddings for {len(text_list)} text(s)")

        client = openai.OpenAI()
        response = client.embeddings.create(
            input=text_list,
            model=EMBEDDING_MODEL
        )

        embeddings = [np.array(item.embedding, dtype=np.float32).tobytes() for item in response.data]

        logging.info(f"Generated {len(embeddings)} embeddings.")
        return embeddings

    except Exception as e:
        logging.error(f"Error generating embeddings: {str(e)}")
        return None  

def process_embeddings(exec_id):
    session = SessionLocal()

    try:
        logging.info(f"Starting embedding process for exec_id: {exec_id}")

        records = get_texts_for_embedding(exec_id)
        if not records:
            logging.info(f"No records to process for exec_id: {exec_id}")
            return

        remaining_records = records

        while remaining_records:
            batch = remaining_records[:BATCH_SIZE]
            texts = [record.content_processed for record in batch]

            embeddings = generate_embeddings(texts)

            if embeddings and len(embeddings) == len(batch):
                update_embeddings(session, batch, embeddings)
                session.commit()
                logging.info(f"Updated {len(batch)} embeddings.")

                remaining_records = remaining_records[BATCH_SIZE:]

            else:
                logging.warning(f"Retrying {len(batch)} records due to embedding failure.")

    except Exception as e:
        logging.error(f"Processing error: {str(e)}")
        session.rollback()
        raise

    finally:
        session.close()
        logging.info("Embedding process completed.")
