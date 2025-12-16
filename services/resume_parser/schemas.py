from pydantic import BaseModel, Field
from typing import List

class ResumeInput(BaseModel):
    tenant_id: str = Field(..., description="Tenant identifier")
    candidate_id: int = Field(..., description="Candidate ID")
    file_url: str = Field(..., description="Resume URL (PDF/DOCX/TXT)")

class ResumeOutput(BaseModel):
    candidate_id: int
    name: str = "N/A"
    email: str = "N/A"
    phone: str = "N/A"
    skills: List[str] = []
    companies_worked: List[str] = []
    job_titles: List[str] = []
    education: List[str] = []
    total_experience_years: float = 0.0
    parsed_summary: str = ""
