import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_FILENAME = os.path.join(MODEL_DIR, "bug_severity_classifier.pkl")
LABEL_ENCODER_FILENAME = os.path.join(MODEL_DIR, "severity_label_encoder.pkl")


data = {
    'bug_description': [
        "Login button disappears after session expiration, preventing all user access.", 
        "Payment fails randomly for 1% of users during high load hours.", 
        "The application crashes when submitting the primary user registration form with empty fields.", 
        "Text alignment in the mobile footer is off by 2 pixels on iOS devices.", 
        "Error message displayed for wrong password is too vague and confusing.", 
        "API returning 500 error on user creation endpoint, blocking new sign-ups.", 
        "Non-essential 'About Us' link broken, accessible via direct URL only.", 
        "Database connection pooling issue, causing occasional deadlocks in production.", 
        "Dropdown menu text wrapping improperly on smaller screens in Chrome.",
        "Missing period at the end of a tooltip description.", 
        "High memory leak detected in the background processing worker.",
        "Report generation hangs indefinitely for large datasets."
    ],
    
    'severity': ['Critical', 'Major', 'Critical', 'Minor', 'Minor', 'Major', 'Trivial', 'Critical', 'Minor', 'Trivial', 'Major', 'Critical']
}
df = pd.DataFrame(data)

X = df['bug_description']
y_raw = df['severity']

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y_raw)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)



bug_severity_pipeline = Pipeline([
    
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=500, ngram_range=(1, 2))),
    
    ('classifier', LogisticRegression(random_state=42, max_iter=2000))
])


print("Starting training of the AI Bug Severity Classifier...")
bug_severity_pipeline.fit(X_train, y_train)
print("Training complete.")


y_pred = bug_severity_pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n--- Model Evaluation ---")
print(f"Test Accuracy: {accuracy:.2f}")
print("Classification Report:")

print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))


if not os.path.exists(os.path.dirname(MODEL_FILENAME)) and os.path.dirname(MODEL_FILENAME):
    os.makedirs(os.path.dirname(MODEL_FILENAME))

try:
    
    joblib.dump(bug_severity_pipeline, MODEL_FILENAME)
  
    joblib.dump(label_encoder, LABEL_ENCODER_FILENAME)
    print(f"\nSuccessfully saved the model pipeline to: {MODEL_FILENAME}")
    print(f"Successfully saved the label encoder to: {LABEL_ENCODER_FILENAME}")
except Exception as e:
    print(f"Error saving model components: {e}")

print("\nReady to use in FastAPI endpoint /ai/bug/analyze.")