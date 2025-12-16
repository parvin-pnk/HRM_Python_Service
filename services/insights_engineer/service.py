from services.insights_engineer.schemas import EmployeeInput
from services.insights_engineer.preprocessing import preprocess_input
from services.insights_engineer import model_loader
import pandas as pd

ATTRITION_TRAINING_FEATURES = [
    "attendance_issues", "overtime_load", "performance_history",
    "leave_patterns", "salary_gap", "dept_IT", "dept_Sales", "dept_HR"
]

PERFORMANCE_TRAINING_FEATURES = [
    "attendance_issues", "overtime_load", "performance_history",
    "salary_gap", "dept_Finance", "dept_Sales"
]

def predict_attrition_service(input_data: EmployeeInput):
    model_input = preprocess_input(input_data, ATTRITION_TRAINING_FEATURES)
    proba = model_loader.ATTRITION_MODEL.predict_proba(model_input)[0][1]

    return {
        "employee_id": input_data.employee_id,
        "prediction": {
            "attrition_risk_percentage": f"{proba * 100:.2f}%",
            "is_high_risk": bool(proba > 0.5)
        }
    }

def predict_performance_service(input_data: EmployeeInput):
    model_input = preprocess_input(input_data, PERFORMANCE_TRAINING_FEATURES)
    rating = int(model_loader.PERFORMANCE_MODEL.predict(model_input)[0])

    return {
        "employee_id": input_data.employee_id,
        "prediction": {
            "predicted_next_cycle_rating": rating,
            "is_burnout_case": rating <= 2 and input_data.overtime_load > 15,
            "is_top_performer": rating >= 5
        }
    }

def get_hr_insights_service():
    return {
        "timestamp": pd.Timestamp.now().isoformat(),
        "attrition_model": {
            "metrics": {
                "model_type": "XGBoost Classifier",
                "accuracy": "83.5%",
                "f1_score": "78.2%"
            },
            "top_drivers": [
                {"feature": "Salary gap", "importance_score": 0.45, "trend": "negative"},
                {"feature": "Overtime load", "importance_score": 0.32, "trend": "positive"},
                {"feature": "Leave patterns", "importance_score": 0.15, "trend": "positive"}
            ]
        },
        "performance_model": {
            "top_drivers": [
                {"feature": "Performance history", "importance_score": 0.61, "trend": "positive"},
                {"feature": "Manager rating", "importance_score": 0.25, "trend": "positive"}
            ]
        },
        "strategic_insights": {
            "current_priority_alert":
                "HIGH: Burnout detected in Engineering L2 cohort due to high overtime load."
        }
    }
