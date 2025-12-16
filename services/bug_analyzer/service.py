from fastapi import HTTPException
from services.bug_analyzer import model_loader
from services.bug_analyzer.schemas import BugInput, BugAnalysisOutput

ROOT_CAUSE_MAP = {
    "Critical": "Likely production data integrity or crash issue.",
    "Major": "Likely a critical path failure or service downtime issue.",
    "Minor": "Likely a UI/UX or non-critical functionality issue.",
    "Trivial": "Likely a cosmetic or documentation issue."
}

def analyze_bug_service(bug: BugInput) -> BugAnalysisOutput:

    if model_loader.bug_model is None or model_loader.severity_encoder is None:
        raise HTTPException(
            status_code=503,
            detail="Bug Analysis service unavailable. Models not loaded."
        )

    try:
        X_new = [bug.bug_description]

        numerical_prediction = model_loader.bug_model.predict(X_new)[0]
        severity_label = model_loader.severity_encoder.inverse_transform(
            [numerical_prediction]
        )[0]

        root_cause = ROOT_CAUSE_MAP.get(
            severity_label, "General software logic error."
        )

        suggested_fix = (
            f"Prioritize fix due to {severity_label} severity. "
            "Reproduce in staging and deploy hotfix if needed."
        )

        return BugAnalysisOutput(
            predicted_severity=severity_label,
            predicted_root_cause=root_cause,
            suggested_fix=suggested_fix
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bug analysis failed: {e}"
        )
