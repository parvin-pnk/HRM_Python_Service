from pydantic import BaseModel, Field
from typing import List, Optional

class CandidateProfile(BaseModel):
    candidate_id: int
    parsed_summary: str
    skills: List[str]
    education: List[str]
    total_experience_years: float

class RankingInput(BaseModel):
    tenant_id: str
    job_id: int
    job_description: str
    candidates: List[CandidateProfile]

class CandidateScore(BaseModel):
    candidate_id: int
    score: float
    matching_skills: List[str]
    reason: str
    weakness: Optional[str] = None
