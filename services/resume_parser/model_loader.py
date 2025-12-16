import spacy
from common.logging_util import log

nlp = None

def load_models():
    global nlp
    try:
        nlp = spacy.load("en_core_web_sm")
        log.info("SpaCy model loaded successfully.")
    except Exception as e:
        log.error(
            "SpaCy model 'en_core_web_sm' not found. "
            "Run: python -m spacy download en_core_web_sm",
            exc_info=True
        )
        nlp = None
