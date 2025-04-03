import numpy as np
from sklearn.decomposition import PCA
import os

SEED = int(os.getenv("SEED", 42))

def compute_pca(embeddings):

    try:
        np.random.seed(SEED)

        pca = PCA(n_components=10, random_state=SEED)
        reduced_embeddings = pca.fit_transform(embeddings)

        return 2, reduced_embeddings 

    except Exception as e:
        raise RuntimeError(f"Error in pca_reduction.py: {str(e)}")
