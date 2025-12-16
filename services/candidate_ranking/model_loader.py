from sentence_transformers import SentenceTransformer
from common.logging_util import log

sbert_model = None

def load_models():
    global sbert_model
    try:
        sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
        log.info("SBERT model loaded successfully for Candidate Ranking.")
    except Exception:
        log.error(
            "SBERT model failed to load. Ensure internet access and model download.",
            exc_info=True
        )
        sbert_model = None
