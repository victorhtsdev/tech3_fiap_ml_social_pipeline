import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.content import Content
from config.database import engine
from models.pipeline_log import PipelineLog
from models.ml_execution import MLExecution
from models.ml_cluster import MLCluster
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def insert_content_dataframe(df, source, execution_id):
    
    if df.empty:
        logging.warning("⚠️ The provided DataFrame is empty. No data inserted.")
        return

    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            content_entry = Content(
                id=execution_id,
                content=row["comment_text"],
                source=source,
                url=row["video_url"],
                user_id=row["channel_title"],  
                user_id2=row["author"], 
                date_posted=row["comment_date"],
                cluster_id=None,
                embeddings=None,
            )
            session.add(content_entry)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                logging.warning(f"⚠️ Duplicate entry detected and skipped for comment: {row['comment_text']}")
                continue  # Continua para o próximo comentário
            except SQLAlchemyError as e:
                session.rollback()
                logging.error(f"❌ Database insertion error: {str(e)}")
                raise  # Propaga o erro para ser tratado na camada superior

        logging.info(f"✅ Content data from {source} inserted successfully with execution_id: {execution_id}")

    except Exception as e:
        logging.error(f"❌ Unexpected error: {str(e)}")
        raise  

    finally:
        session.close()


def insert_pipeline_log(log_id, stage, status, details):
    """Insere um log no pipeline_logs"""
    session = SessionLocal()
    try:
        log_entry = PipelineLog(
            id=log_id,
            stage=stage,
            status=status,
            details=details
        )
        session.add(log_entry)
        session.commit()
        logging.info(f"✅ Log inserido: {stage} - {status} (ID: {log_id})")
    
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"❌ Erro ao inserir log: {str(e)}")
        raise  
    
    finally:
        session.close()


def insert_ml_execution(exec_id, search, date, version):

    session = SessionLocal()
    try:
        execution_entry = MLExecution(
            id=exec_id,
            search=search,
            date=date,
            version=version
        )
        session.add(execution_entry)
        session.commit()
        logging.info(f"✅ Execution registered: {date} - Version {version} - Search: {search} (ID: {exec_id})")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"❌ Error registering execution: {str(e)}")
        raise  

    finally:
        session.close()

def insert_clusters(exec_id, clusters_data: dict):
    session = SessionLocal()
    try:
        clusters_to_insert = []

        for cluster_id, cluster_info in clusters_data["clusters"].items():
            cluster_entry = MLCluster(
                exec_id=exec_id,
                cluster=int(cluster_id),
                topic=cluster_info.get("topic"),
                pattern_found=cluster_info.get("pattern_found"),
                keyword=cluster_info.get("keyword"),
                conclusion=cluster_info.get("conclusion"),
                is_consistent=cluster_info.get("is_consistent"),
                record_count=cluster_info.get("record_count", 0),  
                created_at=datetime.utcnow()
            )

            clusters_to_insert.append(cluster_entry)

        session.add_all(clusters_to_insert)
        session.commit()
        logging.info(f"✅ {len(clusters_to_insert)} clusters inserted successfully.")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"❌ Error inserting clusters: {str(e)}")
        raise  

    finally:
        session.close()