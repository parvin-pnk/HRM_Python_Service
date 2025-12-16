import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import pickle
import numpy as np
import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "performance_model.pkl")

print("Saving model to:", MODEL_PATH)



PERFORMANCE_TRAINING_FEATURES = [
    'attendance_issues',
    'overtime_load',
    'performance_history',
    'salary_gap',
    'dept_Finance',
    'dept_Sales'
]

TARGET_COLUMN = 'Predicted_Rating'



np.random.seed(42)
data = {}

data['attendance_issues'] = np.random.randint(0, 5, 1000)
data['overtime_load'] = np.random.uniform(0.0, 30.0, 1000)
data['performance_history'] = np.random.uniform(2.5, 5.0, 1000)
data['salary_gap'] = np.random.uniform(-0.10, 0.10, 1000)
data['department'] = np.random.choice(
    ['IT', 'Sales', 'HR', 'Finance', 'Marketing'],
    1000,
    p=[0.25, 0.25, 0.15, 0.15, 0.20]
)

df = pd.DataFrame(data)

df = pd.get_dummies(df, columns=['department'], prefix='dept')

for col in ['dept_Finance', 'dept_Sales']:
    if col not in df.columns:
        df[col] = 0



df[TARGET_COLUMN] = (
    3.0
    + (df['performance_history'] * 0.5)
    - (df['attendance_issues'] * 0.2)
    + (df['salary_gap'] * 5)
)

df[TARGET_COLUMN] = (
    df[TARGET_COLUMN]
    .clip(1, 5)
    .round(0)
    .astype(int)
)



X = df[PERFORMANCE_TRAINING_FEATURES]
y = df[TARGET_COLUMN]

X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training Performance Prediction Model...")
performance_model = DecisionTreeRegressor(
    max_depth=5,
    random_state=42
)

performance_model.fit(X_train, y_train)

print(f"Training R² Score: {performance_model.score(X_train, y_train):.4f}")



with open(MODEL_PATH, "wb") as f:
    pickle.dump(performance_model, f)

print("\n✅ Performance model saved successfully!")
print(f"📁 Location: {MODEL_PATH}")
