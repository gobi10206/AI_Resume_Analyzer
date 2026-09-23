# AI Resume Analyzer | AI-Powered Resume Analysis & Career Recommendation System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.92+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3+-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4+-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A modern, production-oriented, full-stack AI platform that analyzes resumes using Natural Language Processing (NLP), evaluates candidates with an explainable 0-100 scoring model, performs 8-point ATS compatibility audits, and generates personalized career roadmaps.

---

## ✨ Key Features

1. **Multi-Format Ingestion**: Drag-and-drop parsing for PDF (`pypdf`, `pdfplumber`), DOCX (`python-docx`), and TXT with OCR scanned PDF fallback (`pytesseract`).
2. **NLP Entity Extraction**: Extracts contact details, LinkedIn/GitHub links, education degrees, GPA, graduation year, work experience, projects, and certifications.
3. **Comprehensive Skill Taxonomy**: 400+ indexed skills across 10 technical categories (Programming Languages, Frameworks, Cloud & DevOps, Databases, ML/AI, Data Engineering, Web Tech, Soft Skills, Tools, Cybersecurity).
4. **Explainable 0-100 Scoring Engine**: Category-wise weighted scoring (Contact 15%, Experience 25%, Skills 25%, Education 15%, Formatting 20%) with actionable strengths and weaknesses.
5. **ATS Compatibility Engine**: 8-point audit covering formatting, section headings, contact completeness, keyword density, table risks, and resume word count.
6. **Semantic Job Matching**: Real-time comparison against custom Job Descriptions using TF-IDF cosine similarity, keyword gap identification, and qualification gap analysis.
7. **Role Fit & Gap Analysis**: Evaluates fit against 12 industry job roles with matching/missing skills and skill gap percentages.
8. **AI Resume Improver**: Rewrites section summaries, experience bullets, and projects into Google XYZ formula format with power verbs and quantifiable metrics.
9. **Personalized Career Roadmap**: 4-phase, 24-week timeline with milestones, recommended courses, capstone projects, and certifications.
10. **Interactive Visual Dashboard**: Animated radial score gauges, category progress bars, Recharts skill distribution charts, and modern responsive dark-mode UI.

---

## 🚀 Quick Start with Docker Compose

Run the entire application stack (PostgreSQL + FastAPI + React Frontend) with one command:

```bash
git clone <repo-url>
cd ai-resume-analyzer
docker compose up --build -d
```

- **Web Application**: Open [http://localhost:3000](http://localhost:3000)
- **Interactive API Documentation**: Open [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 💻 Local Development Setup

### Backend (Python 3.11+)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_server.py
```
*Backend runs on `http://localhost:8000` with automated SQLite persistence.*

### Frontend (Node.js 18+)
```bash
cd frontend
npm install
npm run dev
```
*Frontend runs on `http://localhost:5173`.*

---

## 🧪 Testing & AI Evaluation

Run the complete test suite including precision/recall and monotonicity benchmarks:
```bash
cd backend
python -m pytest tests/ -v
```

---

## 📚 Technical Documentation

- **[System Architecture](docs/ARCHITECTURE.md)**: System design, layers, and database schema.
- **[REST API Specification](docs/API.md)**: Complete request and response specifications for all endpoints.
- **[Setup & Deployment Guide](docs/SETUP.md)**: Local, Docker, and environment configuration instructions.
- **[AI Pipeline Deep Dive](docs/AI_PIPELINE.md)**: Mathematical formulas, NLP models, and ATS scoring weights.

---

## 📄 License
Released under the [MIT License](LICENSE).
