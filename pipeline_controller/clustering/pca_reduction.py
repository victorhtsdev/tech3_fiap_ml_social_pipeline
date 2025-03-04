import numpy as np
from sklearn.decomposition import PCA

def compute_pca(embeddings, min_variance=0.95):
    try:
        pca = PCA().fit(embeddings)
        cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
        num_components = np.argmax(cumulative_variance >= min_variance) + 1
        reduced_embeddings = PCA(n_components=num_components).fit_transform(embeddings)
        return num_components, reduced_embeddings
    except Exception as e:
        raise RuntimeError(f"Error in pca_reduction.py: {str(e)}")
