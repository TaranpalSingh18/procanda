# Procanda

Procanda is an interview-answer evaluation service built with FastAPI and LangGraph.
It scores a candidate answer against a skill and question type, then returns:

- score (0-10)
- reasoning
- confidence (0-1)

## Project Structure

- Backend/: FastAPI app and evaluator logic
- Backend/main.py: API entry point
- Backend/Agent/confidence.py: validation + LLM scoring graph
- Backend/requirements.txt: Python dependencies

## Requirements

- Python 3.10+
- Groq API key

## Environment Variables

Create Backend/.env and add:

GROQ_API_KEY=your_groq_api_key_here

## Setup

From the project root:

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run API

```powershell
cd Backend
uvicorn main:app --reload
```

Default server URL:

- http://127.0.0.1:8000

## API Endpoints

### Health Check

- Method: GET
- Path: /

Response:

```json
{
  "message": "healthy"
}
```

### Evaluate Details

- Method: POST
- Path: /details
- Content-Type: application/json

Request body:

```json
{
  "skill": "Sales Persuasion",
  "question_type": "experience",
  "candidate_answer": "I convinced a hesitant client by understanding their needs and showing ROI."
}
```

Example using PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/details" -ContentType "application/json" -Body '{"skill":"Sales Persuasion","question_type":"experience","candidate_answer":"I convinced a hesitant client by understanding their needs and showing ROI."}'
```

Example response shape:

```json
{
  "skill": "Sales Persuasion",
  "question_type": "experience",
  "candidate_answer": "I convinced a hesitant client by understanding their needs and showing ROI.",
  "score": 8,
  "reasoning": "Strong relevance to sales persuasion with a practical impact-oriented example.",
  "confidence": 0.86
}
```

## Notes

- .gitignore is configured to exclude env files and virtual environments.
- If the model response is not valid JSON, fallback values are returned by the evaluator.
