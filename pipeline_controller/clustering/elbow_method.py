import os
import numpy as np
import faiss

SEED = int(os.getenv("SEED", 42))

def find_best_k(reduced_embeddings, k_min=2, k_max=10):
    try:
        inertia_values = []
        k_values = list(range(k_min, k_max + 1))

        for k in k_values:
            kmeans = faiss.Kmeans(d=reduced_embeddings.shape[1], k=k, niter=300, seed=SEED)
            kmeans.train(reduced_embeddings.astype(np.float32))
            inertia_values.append(kmeans.obj[-1]) 

        variations = np.diff(inertia_values, 2)
        best_k = k_values[np.argmin(variations[:k_max - 2]) + 1]

        return best_k

    except Exception as e:
        raise RuntimeError(f"Error in find_best_k: {str(e)}")
