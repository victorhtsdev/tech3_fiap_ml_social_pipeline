import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config.database import engine
from models.content import Content
from models.content_processed import ContentProcessed
from models.ml_execution import MLExecution
from models.pipeline_log import PipelineLog

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def delete_execution_data(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"🗑️ Iniciando exclusão de dados para exec_id: {exec_id}")

        cp_deleted = session.query(ContentProcessed).filter_by(exec_id=exec_id).delete()
        logging.info(f"🔸 {cp_deleted} registros deletados de content_processed")

        c_deleted = session.query(Content).filter_by(exec_id=exec_id).delete()
        logging.info(f"🔸 {c_deleted} registros deletados de content")

        pl_deleted = session.query(PipelineLog).filter_by(id=exec_id).delete()
        logging.info(f"🔸 {pl_deleted} registros deletados de pipeline_log")

        me_deleted = session.query(MLExecution).filter_by(id=exec_id).delete()
        logging.info(f"🔸 {me_deleted} registros deletados de ml_execution")

        session.commit()
        logging.info(f"✅ Exclusão concluída com sucesso para exec_id: {exec_id}")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"❌ Erro ao deletar dados para exec_id {exec_id}: {str(e)}")
        raise

    finally:
        session.close()
