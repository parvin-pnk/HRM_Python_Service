import re
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import HTTPException

from services.candidate_ranking.schemas import (
    CandidateProfile,
    CandidateScore
)
from services.candidate_ranking import model_loader

def calculate_weighted_score(
    jd_text: str,
    candidate: CandidateProfile
) -> CandidateScore:

    if model_loader.sbert_model is None:
        raise HTTPException(
            status_code=503,
            detail="SBERT model not loaded."
        )

    combined_text = candidate.parsed_summary + " " + " ".join(candidate.skills)

    embeddings = model_loader.sbert_model.encode(
        [jd_text, combined_text]
    )

    jd_vector = embeddings[0].reshape(1, -1)
    candidate_vector = embeddings[1].reshape(1, -1)

    similarity = cosine_similarity(jd_vector, candidate_vector)[0][0]
    similarity_score = similarity * 50.0   

    jd_skills = set(
        re.findall(r"(Python|Django|REST|Java|SQL|AWS|React)", jd_text, re.IGNORECASE)
    )
    candidate_skills = {s.lower() for s in candidate.skills}
    matched_skills = [s for s in jd_skills if s.lower() in candidate_skills]
    skill_match_boost = len(matched_skills) * 5.0

    required_exp = 3.0
    exp_ratio = min(1.0, candidate.total_experience_years / required_exp)
    experience_score = exp_ratio * 30.0  

    education_score = 0.0
    if any(deg in " ".join(candidate.education) for deg in ["B.Tech", "M.Tech", "Engineering"]):
        education_score = 10.0  

    total_score = (
        similarity_score +
        experience_score +
        education_score +
        skill_match_boost
    )

    final_score = round(min(total_score, 100.0), 1)

    reason = f"High similarity ({round(similarity * 100)}%) with {len(matched_skills)} key skill matches."
    weakness = None
    if experience_score < 30.0:
        weakness = "Experience is below the ideal threshold for this role."

    return CandidateScore(
        candidate_id=candidate.candidate_id,
        score=final_score,
        matching_skills=matched_skills,
        reason=reason,
        weakness=weakness
    )


def rank_candidates_service(
    jd_text: str,
    candidates: List[CandidateProfile]
) -> List[CandidateScore]:

    ranked_list = [
        calculate_weighted_score(jd_text, candidate)
        for candidate in candidates
    ]

    ranked_list.sort(key=lambda x: x.score, reverse=True)
    return ranked_list
