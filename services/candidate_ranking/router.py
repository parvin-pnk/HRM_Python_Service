from fastapi import APIRouter
from typing import List

from services.candidate_ranking.schemas import (
    RankingInput,
    CandidateScore
)
from services.candidate_ranking.service import rank_candidates_service
from services.candidate_ranking import model_loader
from common.logging_util import log

router = APIRouter(
    prefix="/ai/ranking",
    tags=["Candidate Ranking"]
)

@router.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "candidate_ranking",
        "sbert_loaded": model_loader.sbert_model is not None
    }

@router.post("/score", response_model=List[CandidateScore])
def rank_candidates(input: RankingInput):
    log.info(
        "Candidate ranking request received",
        extra={
            "payload": {
                "tenant_id": input.tenant_id,
                "job_id": input.job_id,
                "candidate_count": len(input.candidates)
            }
        }
    )

    return rank_candidates_service(
        input.job_description,
        input.candidates
    )
