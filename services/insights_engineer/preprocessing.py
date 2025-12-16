import pandas as pd
from typing import List
from services.insights_engineer.schemas import EmployeeInput

def preprocess_input(data: EmployeeInput, training_features: List[str]):
    df = pd.DataFrame([data.model_dump()])
    df = df.drop(columns=["employee_id", "manager_rating"])

    dummy_df = pd.get_dummies(df["department"], prefix="dept")
    df = pd.concat([df.drop("department", axis=1), dummy_df], axis=1)

    for col in training_features:
        if col not in df.columns:
            df[col] = 0

    df = df[training_features]
    return df.values
