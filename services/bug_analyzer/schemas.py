from pydantic import BaseModel, Field

class BugInput(BaseModel):
    bug_description: str = Field(
        ...,
        description="Detailed bug report, including symptoms and context."
    )

class BugAnalysisOutput(BaseModel):
    predicted_severity: str = Field(
        ..., description="Predicted severity (Critical, Major, Minor, Trivial)."
    )
    predicted_root_cause: str = Field(
        ..., description="Root cause (placeholder / rule-based)."
    )
    suggested_fix: str = Field(
        ..., description="Suggested fix or action."
    )
