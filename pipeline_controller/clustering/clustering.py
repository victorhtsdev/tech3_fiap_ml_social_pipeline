import logging
import json
import sys
import random
import numpy as np
from scipy.spatial.distance import cdist
from sqlalchemy.exc import SQLAlchemyError
from data_storage.data_getter import get_content_data, get_ml_execution_data
from clustering.pca_reduction import compute_pca
from clustering.elbow_method import find_best_k
from clustering.faiss_clustering import run_kmeans_faiss
from ai_services.agents.cluster_evaluator import evaluate_clusters
from data_storage.data_update import update_cluster_ids
from data_storage.data_inserter import insert_clusters 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def clustering_pipeline(exec_id):
    try:
        print(f"🔹 [1/8] Starting clustering process for exec_id: {exec_id}")
        sys.stdout.flush()

        print(f"🔹 [2/8] Fetching ML execution data for exec_id: {exec_id}")
        execution_data = get_ml_execution_data(exec_id)
        sys.stdout.flush()

        if not execution_data:
            print(f"❌ No execution data found for exec_id: {exec_id}")
            return

        topic = execution_data["search"]
        print(f"✅ Search topic retrieved: {topic}")
        sys.stdout.flush()

        print(f"🔹 [3/8] Fetching content and embeddings for exec_id: {exec_id}")
        content_data = get_content_data(exec_id)
        sys.stdout.flush()

        if not content_data:
            print(f"❌ No content found for exec_id: {exec_id}")
            return

        print(f"✅ Retrieved {len(content_data)} content items.")
        sys.stdout.flush()

        print(f"🔹 [4/8] Decoding embeddings...")
        embeddings = np.array([np.frombuffer(record["embeddings"], dtype=np.float32) for record in content_data])
        texts = [record["content"] for record in content_data]
        print(f"✅ Embeddings decoded successfully. Shape: {embeddings.shape}")
        sys.stdout.flush()

        print(f"🔹 [5/8] Applying PCA reduction...")
        num_pca, reduced_embeddings = compute_pca(embeddings)
        print(f"✅ PCA completed. Reduced to {num_pca} dimensions.")
        sys.stdout.flush()

        print(f"🔹 [6/8] Finding the optimal number of clusters...")
        best_k = find_best_k(reduced_embeddings)
        print(f"✅ Optimal K found: {best_k}")
        sys.stdout.flush()
        best_k = 8  # teste
        print(f"🔹 [7/8] Running K-Means clustering...")
        k_values = [best_k]
        clustering_results = {}
        cluster_centroids = {}

        for k in k_values:
            print(f"   - Running K-Means for K={k}...")
            kmeans = run_kmeans_faiss(reduced_embeddings, k)

            labels = kmeans["labels"]
            centroids = kmeans["centroids"]

            clusters_json = {i: [] for i in range(k)}
            cluster_centroids[k] = centroids

            for idx, label in enumerate(labels):
                clusters_json[label].append((texts[idx], reduced_embeddings[idx]))

            clustering_results[k] = clusters_json
            print(f"   ✅ Clustering done for K={k}")
            sys.stdout.flush()

        print(f"🔹 [8/8] Selecting closest samples per cluster...")
        sampled_clusters = {}

        for k in k_values:
            sampled_clusters[k] = {}
            centroids = cluster_centroids[k]

            for cluster_id, data in clustering_results[k].items():
                comments, vectors = zip(*data)  
                vectors = np.array(vectors)

                cluster_size = len(comments)
                
                pct_centroid = 0.4
                pct_random = 0.1

                num_centroid_samples = max(1, int(np.ceil(cluster_size * pct_centroid)))
                num_random_samples = max(1, int(np.ceil(cluster_size * pct_random)))

                num_centroid_samples = min(num_centroid_samples, cluster_size)
                num_random_samples = min(num_random_samples, cluster_size - num_centroid_samples)

                distances = cdist(vectors, [centroids[cluster_id]], metric='cosine').flatten()

                closest_indices = distances.argsort()[:num_centroid_samples]
                closest_samples = [comments[i] for i in closest_indices]

                remaining_indices = list(set(range(cluster_size)) - set(closest_indices))
                random_samples = random.sample(remaining_indices, min(num_random_samples, len(remaining_indices)))

                sampled_clusters[k][cluster_id] = closest_samples + [comments[i] for i in random_samples]

                print(f"🔹 Cluster {cluster_id} (K={k}) - Total: {cluster_size} | Centroid Samples: {num_centroid_samples} | Random Samples: {num_random_samples}")

        print(f"🔹 Sending clusters to LLM for evaluation...")
        llm_inputs = [
            {"clusters": sampled_clusters[k], "current_k": k, "topic": topic}
            for k in k_values
        ]
        sys.stdout.flush()

        llm_outputs = [evaluate_clusters(input_json) for input_json in llm_inputs]

        for i, k in enumerate(k_values):
            print(f"\n🔹 LLM Response for K={k}:")
            for cluster_id in llm_outputs[i]["clusters"]:
                llm_outputs[i]["clusters"][cluster_id]["record_count"] = len(clustering_results[k][int(cluster_id)])
            print(json.dumps(llm_outputs[i], indent=2, ensure_ascii=False))
            sys.stdout.flush()

        print(f"🔹 Inserting LLM evaluation results into the database...")
        for llm_output in llm_outputs:
            insert_clusters(exec_id, llm_output) 

        update_cluster_ids(content_data, labels)

        print(f"✅ Cluster IDs updated in database.")
        sys.stdout.flush()

        print(f"✅ Clustering process completed for exec_id: {exec_id}")
        sys.stdout.flush()

    except SQLAlchemyError as e:
        print(f"❌ Database error: {str(e)}")
        sys.stdout.flush()
        raise RuntimeError(f"Error in clustering_pipeline: {str(e)}")
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.stdout.flush()
        raise RuntimeError(f"Error in clustering_pipeline: {str(e)}")
