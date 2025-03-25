import pickle
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
SVM_MODEL_PATH = os.path.join(MODEL_DIR, "svm_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")

def load_model():
    """Carrega o modelo SVM treinado."""
    with open(SVM_MODEL_PATH, "rb") as f:
        return pickle.load(f)

def load_label_encoder():
    """Carrega o LabelEncoder treinado."""
    with open(ENCODER_PATH, "rb") as f:
        return pickle.load(f)

def save_model(model):
    """Salva um modelo SVM atualizado."""
    with open(SVM_MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

def save_label_encoder(encoder):
    """Salva um LabelEncoder atualizado."""
    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(encoder, f)
