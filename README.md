# Blood Test Report Analyser

## Overview
This project is a FastAPI-based application for analyzing blood test reports using CrewAI agents and Anthropic Claude. It supports background job processing with Celery and Redis.
---

## 🐞 Initial Bugs and Issues (Pre-Celery)

### 1. Dependency and Version Problems
- **Missing dependencies:** The project was missing required packages such as `crewai`, `langchain_anthropic`, `langchain_community`, and others.
- **Version conflicts:** Some packages in `requirements.txt` had overly strict or conflicting version requirements, causing pip install errors.
- **Fix:** Updated and simplified `requirements.txt` to include only top-level packages and let pip resolve sub-dependencies.

### 2. Import Errors
- **Uninitialized LLM:** The Anthropic Claude LLM was not initialized or imported correctly in the agents.
- **Missing imports:** Modules like `PDFLoader` and other CrewAI/LLM components were not imported.
- **Circular imports:** `main.py` and `tasks_celery.py` imported from each other, causing a circular dependency and import errors.
- **Fix:** Added missing imports, ensured all modules import only what they need, and moved the `run_crew` function to a new `crew_runner.py` to break the circular import.

### 3. Environment Variable Issues
- **Missing `.env` file:** The `.env` file was missing or incomplete, so API keys for Anthropic and Serper were not loaded.
- **Incorrect or missing API keys:** The application failed to authenticate with Anthropic Claude or Serper due to missing or incorrect keys.
- **Fix:** Added instructions to create and populate the `.env` file with `ANTHROPIC_API_KEY` and `SERPER_API_KEY`, and ensured the app loads them at runtime.

### 4. File Path and Handling Issues
- **Incorrect file paths:** Uploaded files were not saved or referenced correctly, leading to file not found errors.
- **Premature file deletion:** Uploaded files were deleted before the analysis could be performed.
- **Fix:** Corrected file path handling and removed premature file deletion from the `/analyze` endpoint.

### 5. Switching LLM Providers
- **OpenAI to Anthropic switch:** The project was initially set up for OpenAI, but you wanted to use Anthropic Claude.
- **Model not found errors:** Incorrect model names or API usage caused errors.
- **Fix:** Updated the code to use `langchain_anthropic`, set the correct model name, and ensured the API key was loaded.

### 6. General Project Structure Issues
- **Unclear or missing tool/agent/task structure:** The initial codebase had confusion around how CrewAI agents, tools, and tasks were structured and used.
- **Fix:** Clarified and refactored the structure for agents, tools, and tasks, ensuring each was defined and imported correctly.

---

## 🐞 Bugs Found & How They Were Fixed
- **Celery/Redis connection errors:** Fixed by using the correct Redis URL format and limiting concurrency to avoid free plan connection limits.
- **Circular imports:** Resolved by moving `run_crew` to a separate `crew_runner.py` module.
- **File deletion before task processing:** Fixed by removing premature file deletion in the `/analyze` endpoint.
- **Celery task serialization error:** Fixed by converting CrewAI output to a JSON-serializable format before returning from the task.
- **Missing API keys:** Added checks and instructions for setting `ANTHROPIC_API_KEY` and `SERPER_API_KEY` in `.env`.
- **Serper tool errors:** Fixed by ensuring the Serper API key is set in the environment.

---

## 🚀 Setup Instructions

### 1. Clone the repository
```
git clone <repo-url>
cd debug-assignment/blood-test-analyser-debug
```

### 2. Install dependencies
```
pip install -r requirements.txt
pip install sqlalchemy databases aiosqlite
```

### 3. Set up environment variables
Create a `.env` file in `blood-test-analyser-debug` with:
```
ANTHROPIC_API_KEY=your_anthropic_key_here
SERPER_API_KEY=your_serper_key_here
```

### 4. Set up the database
```
python
>>> from db import metadata, engine
>>> metadata.create_all(engine)
>>> exit()
```

### 5. Start Redis (use Redis Cloud or local Redis)

### 6. Start the FastAPI server
```
uvicorn main:app --reload
```

### 7. Start the Celery worker
```
celery -A tasks_celery:celery_app worker --pool=solo --loglevel=info --concurrency=1
```

---

## 📋 Usage Instructions

### Submit a blood test report for analysis
```
curl -X 'POST' \
  'http://127.0.0.1:8000/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@blood_report_sample.pdf;type=application/pdf' \
  -F 'query=Summarise my Blood Test Report' \
  -F 'username=your_username' \
  -F 'email=your_email@example.com'
```

### Check the result
```
curl -X 'GET' \
  'http://127.0.0.1:8000/result/<task_id>' \
  -H 'accept: application/json'
```

---

## 🛠️ API Documentation

### `POST /analyze`
- **Description:** Upload a blood test PDF and submit a query for analysis.
- **Form Data:**
  - `file`: PDF file
  - `query`: (optional) Query string
  - `username`: (optional) User's username
  - `email`: (optional) User's email
- **Response:**
  - `task_id`: Celery task ID
  - `status`: `queued`
  - `file_processed`: Name of the uploaded file

### `GET /result/{task_id}`
- **Description:** Get the status and result of an analysis job.
- **Response:**
  - `status`: `pending`, `success`, or `failure`
  - `result`: Analysis result (if successful)

---

## ⚡ Notes
- **Concurrency:** On Redis Cloud free plan, keep Celery concurrency low (1–3) to avoid connection errors.
- **Environment:** Ensure `.env` is set up with all required API keys.

- **Troubleshooting:**
  - Check Celery and FastAPI logs for errors.
  - Ensure all dependencies are installed and up to date.
  - If you see serialization errors, ensure your Celery task returns only JSON-serializable data.

---

## 📧 Contact
For help or questions, open an issue or contact the maintainer.
