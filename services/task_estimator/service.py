from fastapi import HTTPException

import services.task_estimator.model_loader as model_loader
from services.task_estimator.logic import classify_complexity

def estimate_task_service(input_data):
    if model_loader.model is None:
        raise HTTPException(
            status_code=503,
            detail="Task Estimator model not loaded"
        )

    X_new = [input_data.task_description]
    estimated_effort = float(model_loader.model.predict(X_new)[0])

    complexity_class, complexity_scale = classify_complexity(estimated_effort)

    return {
        "predicted_effort_hours": round(estimated_effort, 2),
        "complexity_class": complexity_class,
        "complexity_scale_1_10": int(complexity_scale),
    }
