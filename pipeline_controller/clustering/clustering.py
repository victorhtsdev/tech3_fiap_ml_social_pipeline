import logging
import json
import sys
import random
import numpy as np
from scipy.spatial.distance import cdist
from sqlalchemy.exc import SQLAlchemyError
from data_storage.data_getter import get_content_processed_data, get_ml_execution_data
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
        print(f"🔹 [1/6] Starting clustering process for exec_id: {exec_id}")
        sys.stdout.flush()

        execution_data = get_ml_execution_data(exec_id)
        if not execution_data:
            print(f"❌ No execution data found for exec_id: {exec_id}")
            return

        topic = execution_data["search"]
        print(f"✅ Search topic retrieved: {topic}")
        sys.stdout.flush()

        print(f"🔹 [2/6] Fetching content and embeddings for exec_id: {exec_id}")
        content_data = get_content_processed_data(exec_id)
        if not content_data:
            print(f"❌ No content found for exec_id: {exec_id}")
            return

        print(f"✅ Retrieved {len(content_data)} content items.")
        sys.stdout.flush()

        print(f"🔹 [3/6] Decoding embeddings...")
        embeddings = np.array([np.frombuffer(record["embeddings"], dtype=np.float32) for record in content_data])
        texts = [record["sentence"] for record in content_data]
        print(f"✅ Embeddings decoded successfully. Shape: {embeddings.shape}")
        sys.stdout.flush()

        print(f"🔹 [4/6] Applying PCA reduction and finding optimal K...")
        _, reduced_embeddings = compute_pca(embeddings)
        best_k = find_best_k(reduced_embeddings)
        print(f"✅ PCA completed. Initial best K found: {best_k}")
        sys.stdout.flush()

        print(f"🔹 [5/6] Running K-Means clustering for multiple K values...")
        k_values = [k for k in [best_k - 2, best_k - 1, best_k, best_k + 1, best_k + 2] if k >= 2]
        best_silhouette = float('-inf')
        best_k_final = None
        best_clustering_result = None

        for k in k_values:
            print(f"   - Running K-Means for K={k}...")
            kmeans = run_kmeans_faiss(reduced_embeddings, k)

            silhouette_score = kmeans["silhouette_score"]
            print(f"   ✅ Silhouette Score for K={k}: {silhouette_score}")

            if silhouette_score > best_silhouette:
                best_silhouette = silhouette_score
                best_k_final = k
                best_clustering_result = kmeans

        print(f"✅ Best K selected based on Silhouette Score: {best_k_final}")
        sys.stdout.flush()

        print(f"🔹 [6/6] Running final clustering pipeline for K={best_k_final}...")
        labels = best_clustering_result["labels"]
        centroids = best_clustering_result["centroids"]

        clustering_results = {i: [] for i in range(best_k_final)}

        for idx, label in enumerate(labels):
            clustering_results[label].append((texts[idx], reduced_embeddings[idx]))

        print(f"✅ Clustering completed for K={best_k_final}.")
        sys.stdout.flush()

        print(f"🔹 Selecting closest samples per cluster...")
        sampled_clusters = {}

        for cluster_id, data in clustering_results.items():
            comments, vectors = zip(*data)  
            vectors = np.array(vectors)

            cluster_size = len(comments)

            pct_centroid = 0.0
            pct_random = 0.7

            num_centroid_samples = max(1, int(np.ceil(cluster_size * pct_centroid)))
            num_random_samples = max(1, int(np.ceil(cluster_size * pct_random)))

            num_centroid_samples = min(num_centroid_samples, cluster_size)
            num_random_samples = min(num_random_samples, cluster_size - num_centroid_samples)

            distances = cdist(vectors, [centroids[cluster_id]], metric='cosine').flatten()

            closest_indices = distances.argsort()[:num_centroid_samples]
            closest_samples = [comments[i] for i in closest_indices]

            remaining_indices = list(set(range(cluster_size)) - set(closest_indices))
            random_samples = random.sample(remaining_indices, min(num_random_samples, len(remaining_indices)))

            sampled_clusters[cluster_id] = closest_samples + [comments[i] for i in random_samples]

        print(f"🔹 Sending clusters to LLM for evaluation...")
        llm_input = {"clusters": sampled_clusters, "current_k": best_k_final, "topic": topic}
        sys.stdout.flush()

        llm_output = evaluate_clusters(llm_input)

        for cluster_id in llm_output["clusters"]:
            llm_output["clusters"][cluster_id]["record_count"] = len(clustering_results[int(cluster_id)])

        print("\n🔹 LLM Response:")
        print(json.dumps(llm_output, indent=2, ensure_ascii=False))
        sys.stdout.flush()

        print(f"🔹 Inserting LLM evaluation results into the database...")
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
