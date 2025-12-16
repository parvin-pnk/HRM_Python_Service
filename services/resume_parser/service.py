from fastapi import HTTPException

from services.resume_parser.extractor import extract_text_from_url
from services.resume_parser.nlp_engine import nlp_and_regex_parser
import services.resume_parser.model_loader as model_loader


def parse_resume_service(input_data):
    
    if model_loader.nlp is None:
        raise HTTPException(
            status_code=503,
            detail="SpaCy model was not loaded"
        )

    raw_text = extract_text_from_url(input_data.file_url)
    parsed_data = nlp_and_regex_parser(raw_text)
    return parsed_data
