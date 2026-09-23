# AI Resume Analyzer - Setup & Deployment Guide

This document covers running the project locally or via Docker Compose.

---

## Method 1: Docker Compose (Recommended)

Docker Compose starts PostgreSQL, FastAPI Backend, and React Nginx Frontend simultaneously.

### Prerequisites
- Docker & Docker Compose installed.

### Steps
1. Navigate to the project root directory:
   ```bash
   cd ai-resume-analyzer
   ```
2. Launch containers:
   ```bash
   docker compose up --build -d
   ```
3. Access the services:
   - **Web UI**: `http://localhost:3000`
   - **Backend API Docs**: `http://localhost:8000/docs`
   - **PostgreSQL Database**: `localhost:5432` (User: `resume_user`, DB: `resume_db`)

---

## Method 2: Local Development Setup

### Backend Setup (Python 3.11+)
1. Enter backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python run_server.py
   ```
   *The backend starts at `http://localhost:8000` with automated SQLite persistence.*

### Frontend Setup (Node.js 18+)
1. Enter frontend folder:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   *The frontend starts at `http://localhost:5173`.*

---

## Running Automated Tests
From the `backend` folder, execute the automated test suite:
```bash
python -m pytest tests/ -v
```
Or execute using the built-in test runner:
```bash
python -c "
import glob, sys
sys.path.insert(0, '.')
for t in sorted(glob.glob('tests/test_*.py')):
    m = __import__(t.replace('/', '.').replace('.py', ''), fromlist=['*'])
    for a in dir(m):
        if a.startswith('test_'): getattr(m, a)()
print('All tests completed successfully.')
"
```
