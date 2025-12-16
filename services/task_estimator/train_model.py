import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
import joblib
import os

data = {
    "task_title": [
        "Implement user login endpoint",
        "Fix critical bug in payment gateway",
        "Update CSS for homepage footer",
        "Set up new database migration",
        "Refactor legacy auth service code",
        "Add simple unit test for utils",
        "Investigate production outage cause",
        "Write documentation for new API",
        "Optimize slow SQL query in reporting",
        "Add caching layer to user service",
    ],
    "actual_effort_hours": [4.2, 8.5, 1.1, 6.0, 12.3, 0.7, 10.5, 3.1, 5.5, 7.8],
}

df = pd.DataFrame(data)

X = df["task_title"]
y = df["actual_effort_hours"]

X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_features=100)),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
])

pipeline.fit(X_train, y_train)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "effort_estimator_model.pkl")
joblib.dump(pipeline, MODEL_PATH)

print(f" Model saved to {MODEL_PATH}")
