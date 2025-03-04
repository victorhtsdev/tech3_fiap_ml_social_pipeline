import faiss
import numpy as np

def run_kmeans_faiss(embeddings, k):
    try:
        kmeans = faiss.Kmeans(d=embeddings.shape[1], k=k, niter=300, nredo=10, spherical=True)
        kmeans.train(embeddings)

        _, labels = kmeans.index.search(embeddings, 1)

        centroids = np.array(kmeans.centroids)

        return {
            "labels": labels.flatten(),
            "centroids": centroids
        }

    except Exception as e:
        raise RuntimeError(f"Error in faiss_clustering.py: {str(e)}")
