import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_DEFAULT_PATH = os.path.join(BASE_DIR, "models")
MODEL_DIR = os.getenv("MODEL_DIR", LOCAL_DEFAULT_PATH)


def load_model(filename):
    """Carrega um modelo treinado a partir do nome do arquivo."""
    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, "rb") as f:
        return pickle.load(f)

def load_label_encoder(filename):
    """Carrega um LabelEncoder treinado a partir do nome do arquivo."""
    encoder_path = os.path.join(MODEL_DIR, filename)
    with open(encoder_path, "rb") as f:
        return pickle.load(f)

def save_model(model, filename):
    """Salva um modelo treinado no arquivo informado."""
    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

def save_label_encoder(encoder, filename):
    """Salva um LabelEncoder no arquivo informado."""
    encoder_path = os.path.join(MODEL_DIR, filename)
    with open(encoder_path, "wb") as f:
        pickle.dump(encoder, f)

def load_pca(filename):
    """Carrega um objeto PCA salvo."""
    pca_path = os.path.join(MODEL_DIR, filename)
    with open(pca_path, "rb") as f:
        return pickle.load(f)

def save_pca(pca, filename):
    """Salva um objeto PCA no arquivo informado."""
    pca_path = os.path.join(MODEL_DIR, filename)
    with open(pca_path, "wb") as f:
        pickle.dump(pca, f)