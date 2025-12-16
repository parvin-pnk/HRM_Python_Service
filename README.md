HOW TO RUN Python Services

Create env is better for library version conflict
Step 1: pip install -r requirements.txt
Step 2: python -m spacy download en_core_web_sm
Step 3: uvicorn main:app --reload --port 8001

