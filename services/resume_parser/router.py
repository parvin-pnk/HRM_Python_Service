from fastapi import APIRouter
from services.resume_parser.schemas import ResumeInput, ResumeOutput
from services.resume_parser.service import parse_resume_service

router = APIRouter(
    prefix="/ai/resume",
    tags=["Resume Parser"]
)

@router.get("/health")
def health():
    from services.resume_parser.model_loader import nlp
    return {
        "status": "UP",
        "service": "resume_parser",
        "nlp_model_loaded": nlp is not None
    }

@router.post("/parse", response_model=ResumeOutput)
def parse_resume(input: ResumeInput):
    parsed = parse_resume_service(input)
    return ResumeOutput(
        candidate_id=input.candidate_id,
        **parsed
    )
