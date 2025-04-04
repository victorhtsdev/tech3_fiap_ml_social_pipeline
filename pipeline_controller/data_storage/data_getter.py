from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from config.database import engine
from models.ml_execution import MLExecution
from models.content_processed import ContentProcessed
from models.pipeline_log import PipelineLog
from models.content import Content
import logging
from sqlalchemy.sql import func
import numpy as np
from data_processing.pca_reduction import compute_pca
from collections import Counter
from data_processing.text_cleaning import clean_for_word_cloud,normalize_text
from config.category_colors import get_category_colors_list
import re
import random
from models.ml_model import MLModel
from models.model_metric import ModelMetric
from models.class_metric import ClassMetric
from collections import defaultdict
from ml_classification.model_manager import load_pca

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

def get_ml_execution_data(exec_id: str = None):
    session = SessionLocal()
    try:
        if exec_id:
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
        else:
            logging.info("Fetching all ML execution data")
            results = session.query(MLExecution).all()
            return [
                {
                    "id": str(record.id),
                    "search": record.search,
                    "date": record.date,
                    "version": record.version
                }
                for record in results
            ]

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
            ContentProcessed.label,  
            ContentProcessed.sentiment,
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
                "label": record.label,  
                "sentiment": record.sentiment 
            }
            for record in processed_records
        ]

    except SQLAlchemyError as e:
        logging.error(f"Database error in get_content_processed_data: {str(e)}")
        raise RuntimeError(f"Error in get_content_processed_data: {str(e)}")

    finally:
        session.close()


def get_latest_ml_execution():
    session = SessionLocal()
    try:
        logging.info("Fetching latest ML execution data for each unique search")

        subquery = (
            session.query(
                MLExecution.search,
                func.max(MLExecution.date).label("latest_date")
            )
            .group_by(MLExecution.search)
            .subquery()
        )

        results = (
            session.query(MLExecution)
            .join(subquery, (MLExecution.search == subquery.c.search) & (MLExecution.date == subquery.c.latest_date))
            .order_by(desc(MLExecution.date))
            .all()
        )

        return [
            {
                "id": str(record.id),
                "search": record.search,
                "date": record.date,
                "classification_model_version": record.classification_model_version,
                "classification_model_name": record.classification_model_name,
                "classification_model_type": record.classification_model_type,
                "date_ranges": record.date_ranges
            }
            for record in results
        ]

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_latest_ml_execution: {str(e)}")
        raise RuntimeError(f"Error in get_latest_ml_execution: {str(e)}")

    finally:
        session.close()

STAGES = [
    "Data Collection",
    "Preprocessing Data",
    "Embedding Generation",
    "ML Classification",
    "Pipeline Execution"
]

DEFAULT_STATUS = "Not Started"

def get_pipeline_status(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"Fetching execution data for exec_id: {exec_id}")

        query_results = (
            session.query(PipelineLog)
            .filter(PipelineLog.id == exec_id)
            .order_by(PipelineLog.timestamp.asc())
            .all()
        )

        stage_status = {}

        for record in query_results:
            stage_status[record.stage] = record.status

        if not stage_status:
            return {
                "execution_id": exec_id,
                "stages": [{"name": stage, "status": DEFAULT_STATUS} for stage in STAGES]
            }

        if any(status == "Error" for stage, status in stage_status.items() if stage != "Pipeline Execution"):
            stage_status["Pipeline Execution"] = "Error"

        response = {
            "execution_id": exec_id,
            "stages": [
                {"name": stage, "status": stage_status.get(stage, DEFAULT_STATUS)}
                for stage in STAGES
            ]
        }

        return response

    except Exception as e:
        logging.error(f"Error fetching execution status: {str(e)}")
        return {
            "execution_id": exec_id,
            "stages": [{"name": stage, "status": DEFAULT_STATUS} for stage in STAGES]
        }

    finally:
        session.close()

def get_ml_executions_by_search(search: str):
    session = SessionLocal()
    try:
        search_upper = search.upper()
        logging.info(f"Fetching all ML execution records with search = {search_upper}")

        results = (
            session.query(MLExecution)
            .filter(func.upper(MLExecution.search) == search_upper)  
            .order_by(MLExecution.date.desc())
            .all()
        )

        if not results:
            logging.warning(f"No ML execution records found for search: {search_upper}")
            return []

        return [
            {
                "id": str(record.id),
                "search": record.search,
                "date": record.date,
                "classification_model_version": record.classification_model_version,
                "classification_model_name": record.classification_model_name,
                "classification_model_type": record.classification_model_type,
                "date_ranges": record.date_ranges
            }
            for record in results
        ]

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_ml_executions_by_search: {str(e)}")
        raise RuntimeError(f"Error in get_ml_executions_by_search: {str(e)}")

    finally:
        session.close()

def get_embeddings_by_exec_id(exec_id, max_samples=100):
    session = SessionLocal()
    try:
        logging.info(f"🔍 Fetching embeddings for exec_id: {exec_id}")

        records = session.query(
            ContentProcessed.sentence,
            ContentProcessed.embeddings,
            ContentProcessed.label,
            ContentProcessed.content_id  
        ).filter(ContentProcessed.exec_id == exec_id).all()

        if not records:
            logging.warning(f"⚠️ No embeddings found for exec_id: {exec_id}")
            return []

        labels_to_exclude = {}
        category_dict = {}

        for record in records:
            if record.embeddings and record.label not in labels_to_exclude:
                if record.label not in category_dict:
                    category_dict[record.label] = []
                category_dict[record.label].append((record.sentence, record.embeddings, record.content_id)) 

        max_category_size = max(len(items) for items in category_dict.values())

        selected_sentences = []
        selected_embeddings = []
        selected_labels = []
        selected_content_ids = []

        for label, items in category_dict.items():
            category_size = len(items)
            proportion = category_size / max_category_size
            num_samples = max(1, int(proportion * max_samples))

            sampled_items = random.sample(items, min(num_samples, len(items)))

            for sentence, embedding, content_id in sampled_items:
                selected_sentences.append(sentence)
                selected_embeddings.append(np.frombuffer(embedding, dtype=np.float32))
                selected_labels.append(label)
                selected_content_ids.append(content_id)

        if len(selected_embeddings) == 0:
            logging.warning(f"⚠️ No data left after sampling for exec_id: {exec_id}")
            return []

        selected_embeddings = np.array(selected_embeddings)

        model_info = get_model_info_from_execution(exec_id)
        if not model_info:
            raise ValueError("❌ Could not retrieve model info from execution.")

        model_type = model_info["model_type"].lower()
        model_version = model_info["model_version"]
        pca_filename = f"pca_{model_type}_v{model_version}.pkl"

        try:
            pca = load_pca(pca_filename)
            reduced_embeddings = pca.transform(selected_embeddings)
            logging.info(f"📦 PCA successfully applied using {pca_filename}")
        except FileNotFoundError:
            reduced_embeddings = selected_embeddings
            logging.info("ℹ️ PCA not found. Using original embeddings.")

        response_data = [
            {
                "sentence": selected_sentences[i],
                "embedding": reduced_embeddings[i].tolist(), 
                "label": selected_labels[i],
                "content_id": selected_content_ids[i]
            }
            for i in range(len(selected_sentences))
        ]

        logging.info(f"✅ Successfully processed {len(response_data)} embeddings for exec_id: {exec_id}")
        return response_data

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_embeddings_by_exec_id: {str(e)}")
        raise RuntimeError(f"Error in get_embeddings_by_exec_id: {str(e)}")

    finally:
        session.close()

def get_svm_category_counts(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"🔍 Fetching SVM category counts for exec_id: {exec_id}")

        labels_to_exclude = {}

        records = session.query(ContentProcessed.label).filter(
            ContentProcessed.exec_id == exec_id,
            ~ContentProcessed.label.in_(labels_to_exclude)
        ).all()

        if not records:
            logging.warning(f"⚠️ No valid predictions found for exec_id: {exec_id}")
            return []

        category_counts = {}
        for record in records:
            label = record.label
            category_counts[label] = category_counts.get(label, 0) + 1

        result = sorted(
            [{"label": label, "count": count} for label, count in category_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )

        logging.info(f"✅ Successfully counted {len(result)} categories for exec_id: {exec_id}")
        return result

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_svm_category_counts: {str(e)}")
        raise RuntimeError(f"Error in get_svm_category_counts: {str(e)}")

    finally:
        session.close()

CUSTOM_STOPWORDS = {
    "pra", "kkk", "kkkk", "kkkkk", "tá", "ta", "eh", "aí", "ai", "q", "vc", "tipo",
    "né", "to", "serio", "sério", "mano", "pô", "oxe", "uai", "vcs", "mt", "tb", "tbm",
    "blz", "vlw", "aff", "ok", "haha", "rs", "rsrs", "rsrsrs", "so", "só", "eai"
}

def get_word_cloud_data(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"🔍 Generating word cloud data for exec_id: {exec_id}")

        records = session.query(ContentProcessed.sentence, ContentProcessed.label).filter(
            ContentProcessed.exec_id == exec_id
        ).all()

        if not records:
            logging.warning(f"⚠️ No sentences found for exec_id: {exec_id}")
            return []

        word_frequencies = {}
        for sentence, label in records:
            cleaned = clean_for_word_cloud(sentence)
            words = cleaned.split()
            filtered_words = [w for w in words if w not in CUSTOM_STOPWORDS]
            if label not in word_frequencies:
                word_frequencies[label] = Counter()
            word_frequencies[label].update(filtered_words)

        label_counts = {
            label: sum(counter.values())
            for label, counter in word_frequencies.items()
        }

        sorted_labels = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)

        ordered_result = [
            {
                "label": label,
                "words": [{"word": word, "count": count} for word, count in word_frequencies[label].most_common(20)]
            }
            for label, _ in sorted_labels
        ]

        logging.info(f"✅ Word cloud data successfully generated for exec_id: {exec_id}")
        return ordered_result

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_word_cloud_data: {str(e)}")
        raise RuntimeError(f"Error in get_word_cloud_data: {str(e)}")
    finally:
        session.close()

def get_category_colors(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"Fetching classification model type for exec_id: {exec_id}")

        ml_execution = session.query(MLExecution).filter_by(id=exec_id).first()

        if not ml_execution:
            logging.warning(f"⚠️ No record found for exec_id: {exec_id}")
            return {"error": "Exec ID not found"}, 404

        classification_model_type = ml_execution.classification_model_type

        colors = get_category_colors_list(classification_model_type)

        if not colors:
            logging.warning(f"⚠️ No color palette found for '{classification_model_type}'")
            return {"error": f"Color palette not found for '{classification_model_type}'"}, 404

        return colors

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_category_colors: {str(e)}")
        return {"error": f"Database error: {str(e)}"}, 500

    finally:
        session.close()


def get_content_highlight(exec_id, content_id):
    session = SessionLocal()
    try:
        logging.info(f"Fetching content for exec_id: {exec_id}, content_id: {content_id}")

        content_record = session.query(Content).filter_by(exec_id=exec_id, content_id=content_id).first()
        if not content_record:
            logging.warning(f"⚠️ No content found for exec_id: {exec_id}, content_id: {content_id}")
            return {"error": "Content not found"}, 404

        processed_sentences = session.query(ContentProcessed).filter_by(exec_id=exec_id, content_id=content_id).all()
        if not processed_sentences:
            logging.warning(f"⚠️ No processed sentences found for exec_id: {exec_id}, content_id: {content_id}")
            return {"error": "No processed sentences found"}, 404

        category_colors = get_category_colors(exec_id)
        highlights = []
        content_text = content_record.content
        normalized_content_text = normalize_text(content_text)

        for sentence_obj in processed_sentences:
            fragment = sentence_obj.sentence.strip()
            label = sentence_obj.label.strip() if sentence_obj.label else "Uncategorized"

            color = category_colors.get(label, "#000000")

            words = fragment.split()
            if not words:
                continue  

            first_word = words[0]  
            last_word = words[-1]  

            first_match = re.search(re.escape(first_word), content_text, re.IGNORECASE)
            last_match = re.search(re.escape(last_word), content_text, re.IGNORECASE)

            if first_match and last_match:
                start = first_match.start()
                end = last_match.end()

                highlights.append({
                    "content_id": content_id,
                    "processed_id": sentence_obj.processed_id,
                    "fragment": fragment,
                    "label": label,
                    "color": color,
                    "start": start,
                    "end": end
                })
                logging.info(f"✅ Highlight encontrado: {fragment} ({start}-{end})")
            else:
                logging.warning(f"⚠️ Não encontrou: {fragment} dentro do content_id {content_id}")

        return {
            "content_id": content_id,
            "content": content_text,
            "highlights": highlights
        }

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_content_highlight: {str(e)}")
        return {"error": f"Database error: {str(e)}"}, 500

    finally:
        session.close()

def get_models_info():
    session = SessionLocal()
    try:
        logging.info("Fetching model types and models grouped by type")

        models = session.query(
            MLModel.id,
            MLModel.model_name,
            MLModel.model_version,
            MLModel.model_type,
            MLModel.is_recommended
        ).order_by(desc(MLModel.model_version)).all()

        if not models:
            return {"types": [], "models": {}}

        types = sorted(set(m.model_type for m in models if m.model_type))
        grouped_models = {}

        for t in types:
            grouped_models[t] = [
                {
                    "id": str(m.id),
                    "label": f"{m.model_name} - v{m.model_version}",
                    "is_recommended": m.is_recommended
                }
                for m in models if m.model_type == t
            ]

        return {
            "types": types,
            "models": grouped_models
        }

    except SQLAlchemyError as e:
        logging.error(f"Database error in get_models_info: {str(e)}")
        raise RuntimeError("Error fetching models info")

    finally:
        session.close()

def get_model_info_from_execution(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"🔍 Fetching model info from MLExecution for exec_id: {exec_id}")

        execution = session.query(
            MLExecution.classification_model_version,
            MLExecution.classification_model_name,
            MLExecution.classification_model_type
        ).filter(MLExecution.id == exec_id).first()

        if not execution:
            logging.warning(f"⚠️ No MLExecution found for exec_id: {exec_id}")
            return None

        return {
            "model_version": execution.classification_model_version,
            "model_name": execution.classification_model_name,
            "model_type": execution.classification_model_type
        }

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_model_info_from_execution: {str(e)}")
        raise RuntimeError(f"Error fetching model info from MLExecution: {str(e)}")

    finally:
        session.close()

def get_model_metrics_grouped():
    session = SessionLocal()
    try:
        logging.info("🔍 Fetching model metrics grouped by type and version")

        models = session.query(MLModel).order_by(MLModel.model_type, MLModel.model_version).all()
        model_metrics = session.query(ModelMetric).all()
        class_metrics = session.query(ClassMetric).all()

        grouped = defaultdict(lambda: defaultdict(list))

        for model in models:
            model_id = str(model.id)
            model_type = model.model_type
            version = model.model_version
            name = model.model_name

            metric = next((m for m in model_metrics if str(m.model_id) == model_id), None)
            classes = [c for c in class_metrics if str(c.model_id) == model_id]

            grouped[model_type][version].append({
                "model_id": model_id,
                "model_name": name,
                "is_recommended": model.is_recommended,
                "global_metrics": {
                    "accuracy": metric.accuracy if metric else None,
                    "macro_f1": metric.macro_f1 if metric else None,
                    "weighted_f1": metric.weighted_f1 if metric else None,
                },
                "class_metrics": [
                    {
                        "class_name": c.class_name,
                        "f1_score": c.f1_score
                    } for c in classes
                ]
            })

        return grouped

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error while fetching model metrics: {str(e)}")
        raise RuntimeError("Error while fetching model metrics")

    finally:
        session.close()

def get_sentences_by_label_grouped(exec_id, label):
    session = SessionLocal()
    try:
        logging.info(f"🔍 Fetching grouped label sentences for exec_id: {exec_id}, label: {label}")

        results = (
            session.query(
                ContentProcessed.sentence,
                ContentProcessed.processed_id,
                ContentProcessed.label,
                Content.content_id,
                Content.exec_id,
                Content.content
            )
            .join(Content, (ContentProcessed.exec_id == Content.exec_id) & (ContentProcessed.content_id == Content.content_id))
            .filter(
                ContentProcessed.exec_id == exec_id,
                ContentProcessed.label == label
            )
            .order_by(ContentProcessed.content_id, ContentProcessed.processed_id)
            .all()
        )

        if not results:
            logging.warning(f"⚠️ No results found for exec_id={exec_id}, label={label}")
            return []

        grouped_data = {}
        for r in results:
            key = (r.exec_id, r.content_id)
            if key not in grouped_data:
                grouped_data[key] = {
                    "content_id": r.content_id,
                    "label": r.label,
                    "original_comment": r.content,
                    "sentences": []
                }
            grouped_data[key]["sentences"].append({
                "processed_id": r.processed_id,
                "sentence": r.sentence
            })

        return list(grouped_data.values())

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_sentences_by_label_grouped: {str(e)}")
        raise RuntimeError(f"Error in get_sentences_by_label_grouped: {str(e)}")
    finally:
        session.close()

def get_time_series_label_count(exec_id):
    session = SessionLocal()
    try:
        logging.info(f"📊 Fetching time series data for exec_id: {exec_id}")

        ml_execution = session.query(MLExecution).filter_by(id=exec_id).first()
        if not ml_execution:
            logging.warning("⚠️ MLExecution not found")
            return []

        model_type = ml_execution.classification_model_type
        category_colors = get_category_colors_list(model_type)

        results = (
            session.query(
                ContentProcessed.label,
                func.date(Content.date_posted).label("date"),
                func.count().label("count")
            )
            .join(Content, (ContentProcessed.exec_id == Content.exec_id) & (ContentProcessed.content_id == Content.content_id))
            .filter(ContentProcessed.exec_id == exec_id)
            .group_by(ContentProcessed.label, func.date(Content.date_posted))
            .order_by(func.date(Content.date_posted))
            .all()
        )

        response = []
        for label, date, count in results:
            color = category_colors.get(label, "#000000")
            response.append({
                "label": label,
                "date": date.isoformat(),
                "count": count,
                "color": color
            })

        logging.info(f"✅ Time series data ready for exec_id: {exec_id} ({len(response)} points)")
        return response

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error in get_time_series_data: {str(e)}")
        raise RuntimeError(f"Error in get_time_series_data: {str(e)}")
    finally:
        session.close()