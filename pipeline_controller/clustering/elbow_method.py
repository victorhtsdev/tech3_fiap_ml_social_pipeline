import numpy as np
from sklearn.cluster import KMeans

def find_best_k(embeddings, k_min=2, k_max=15):
    try:
        inertia = []
        k_values = list(range(k_min, k_max + 1))

        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(embeddings)
            inertia.append(kmeans.inertia_)

        variations = np.diff(inertia)
        best_k = k_values[np.argmin(variations[:k_max-2]) + 1]
        return best_k
    except Exception as e:
        raise RuntimeError(f"Error in elbow_method.py: {str(e)}")
