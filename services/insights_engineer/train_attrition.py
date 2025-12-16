import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as np
import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "attrition_model.pkl")

print("Saving model to:", MODEL_PATH)



ATTRITION_TRAINING_FEATURES = [
    'attendance_issues',
    'overtime_load',
    'performance_history',
    'leave_patterns',
    'salary_gap',
    'dept_IT',
    'dept_Sales',
    'dept_HR'
]

TARGET_COLUMN = 'Attrition_Risk'


np.random.seed(42)
data = {}

data['attendance_issues'] = np.random.randint(0, 10, 1000)
data['overtime_load'] = np.random.uniform(0.0, 30.0, 1000)
data['performance_history'] = np.random.uniform(2.5, 5.0, 1000)
data['leave_patterns'] = np.random.uniform(0.0, 2.0, 1000)
data['salary_gap'] = np.random.uniform(-0.15, 0.15, 1000)
data['department'] = np.random.choice(
    ['IT', 'Sales', 'HR', 'Finance', 'Marketing'],
    1000,
    p=[0.25, 0.25, 0.15, 0.15, 0.20]
)

df = pd.DataFrame(data)
df = pd.get_dummies(df, columns=['department'], prefix='dept')

for col in ['dept_IT', 'dept_Sales', 'dept_HR']:
    if col not in df.columns:
        df[col] = 0

df[TARGET_COLUMN] = (
    (df['attendance_issues'] > 5) |
    (df['overtime_load'] > 20) |
    (df['salary_gap'] < -0.05)
).astype(int)


X = df[ATTRITION_TRAINING_FEATURES]
y = df[TARGET_COLUMN]

X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training Attrition Model...")
attrition_model = LogisticRegression(
    solver='liblinear',
    random_state=42
)
attrition_model.fit(X_train, y_train)

print(f"Training Accuracy: {attrition_model.score(X_train, y_train):.4f}")



with open(MODEL_PATH, "wb") as f:
    pickle.dump(attrition_model, f)

print("\n✅ Model saved successfully!")
print(f"📁 Location: {MODEL_PATH}")
