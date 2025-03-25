import os
import numpy as np
import faiss

SEED = int(os.getenv("SEED", 42))


def find_best_k(reduced_embeddings, k_min=2, k_max=9):
    try:
        inertia_values = []
        k_values = list(range(k_min, k_max + 1))

        for k in k_values:
            kmeans = faiss.Kmeans(
                d=reduced_embeddings.shape[1], 
                k=k, 
                niter=400, 
                nredo=50, 
                spherical=True, 
                seed=SEED
            )
            kmeans.train(reduced_embeddings.astype(np.float32))
            inertia_values.append(kmeans.obj[-1])  

        optimal_k = k_values[np.diff(inertia_values, 2).argmin() + 1]

        return optimal_k

    except Exception as e:
        raise RuntimeError(f"Erro em find_best_k: {str(e)}")