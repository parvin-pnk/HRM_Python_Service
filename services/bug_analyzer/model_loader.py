import os
import joblib
from common.logging_util import log

import os
import joblib
from common.logging_util import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

BUG_MODEL_FILE = os.path.join(MODEL_DIR, "bug_severity_classifier.pkl")
ENCODER_FILE = os.path.join(MODEL_DIR, "severity_label_encoder.pkl")



bug_model = None
severity_encoder = None

def load_models():
    global bug_model, severity_encoder

    if not (os.path.exists(BUG_MODEL_FILE) and os.path.exists(ENCODER_FILE)):
        log.warning("Bug Analyzer models not found. Train models to enable this service.")
        return

    try:
        bug_model = joblib.load(BUG_MODEL_FILE)
        severity_encoder = joblib.load(ENCODER_FILE)
        log.info("Bug Analyzer models loaded successfully.")
    except Exception as e:
        log.error("Failed to load bug analyzer models", exc_info=True)
        raise RuntimeError(f"Model loading failed: {e}")
