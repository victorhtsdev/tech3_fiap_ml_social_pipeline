import os
import faiss
import numpy as np
import random
from sklearn.metrics import silhouette_score

SEED = int(os.getenv("SEED", 42))

def run_kmeans_faiss(reduced_embeddings, k):
    try:
        np.random.seed(SEED)
        random.seed(SEED)
        faiss.rand(SEED)

        reduced_embeddings = np.ascontiguousarray(reduced_embeddings, dtype=np.float32)

        kmeans = faiss.Kmeans(
            d=reduced_embeddings.shape[1], 
            k=k, 
            niter=300, 
            nredo=50, 
            spherical=True
        )

        kmeans.seed = SEED
        kmeans.train(reduced_embeddings)

        _, labels = kmeans.index.search(reduced_embeddings, 1)
        centroids = np.array(kmeans.centroids)

        silhouette = silhouette_score(reduced_embeddings, labels.flatten(), metric='cosine')

        return {
            "labels": labels.flatten(),
            "centroids": centroids,
            "silhouette_score": silhouette
        }

    except Exception as e:
        raise RuntimeError(f"Error in run_kmeans_faiss: {str(e)}")
