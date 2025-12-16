import os
import pickle
from common.logging_util import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

ATTRITION_MODEL_PATH = os.path.join(MODEL_DIR, "attrition_model.pkl")
PERFORMANCE_MODEL_PATH = os.path.join(MODEL_DIR, "performance_model.pkl")

ATTRITION_MODEL = None
PERFORMANCE_MODEL = None


class PlaceholderModel:
    def __init__(self, task: str):
        self.task = task

    def predict_proba(self, X):
        return [[0.85, 0.15]] * len(X)

    def predict(self, X):
        if self.task == "performance":
            if X[0][2] > 0.8:
                return [5]
            elif X[0][1] > 10 and X[0][0] > 2:
                return [2]
            return [4]
        return [0]


def load_models():
    global ATTRITION_MODEL, PERFORMANCE_MODEL

    try:
        with open(ATTRITION_MODEL_PATH, "rb") as f:
            ATTRITION_MODEL = pickle.load(f)
        log.info(f"Attrition model loaded from {ATTRITION_MODEL_PATH}")
    except FileNotFoundError:
        ATTRITION_MODEL = PlaceholderModel("attrition")
        log.warning("Attrition model not found. Using placeholder model.")

    try:
        with open(PERFORMANCE_MODEL_PATH, "rb") as f:
            PERFORMANCE_MODEL = pickle.load(f)
        log.info(f"Performance model loaded from {PERFORMANCE_MODEL_PATH}")
    except FileNotFoundError:
        PERFORMANCE_MODEL = PlaceholderModel("performance")
        log.warning("Performance model not found. Using placeholder model.")
