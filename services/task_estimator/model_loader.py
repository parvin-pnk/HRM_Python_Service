import joblib
import os
from common.logging_util import log

model = None

def load_models():
    global model

    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "models", "effort_estimator_model.pkl")

    if not os.path.exists(model_path):
        log.error(f"Task Estimator model not found at {model_path}")
        model = None
        return

    try:
        model = joblib.load(model_path)
        log.info("Task Estimator model loaded successfully.")
    except Exception as e:
        log.error("Failed to load Task Estimator model", exc_info=True)
        model = None
