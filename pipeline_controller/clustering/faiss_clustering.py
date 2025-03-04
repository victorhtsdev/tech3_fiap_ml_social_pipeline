import faiss
import numpy as np
import random

def run_kmeans_faiss(embeddings, k, seed=42):
    try:
        np.random.seed(seed)
        random.seed(seed)
        faiss.rand(seed)
        
        kmeans = faiss.Kmeans(
            d=embeddings.shape[1], 
            k=k, 
            niter=300, 
            nredo=50, 
            spherical=True
        )

        kmeans.seed = seed 

        kmeans.train(embeddings)

        _, labels = kmeans.index.search(embeddings, 1)

        centroids = np.array(kmeans.centroids)

        return {
            "labels": labels.flatten(),
            "centroids": centroids
        }

    except Exception as e:
        raise RuntimeError(f"Error in faiss_clustering.py: {str(e)}")
