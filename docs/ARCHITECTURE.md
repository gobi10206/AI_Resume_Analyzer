# AI Resume Analyzer - System Architecture

## 1. High-Level Architectural Overview

The **AI Resume Analyzer** is an end-to-end full-stack platform designed to ingest unstructured resumes in multiple document formats (PDF, DOCX, TXT), perform robust text normalization and NLP entity extraction, evaluate candidates against a multi-factor 0-100 explainable scoring model, verify applicant tracking system (ATS) compliance, and generate personalized career recommendations and roadmaps.

```
┌────────────────────────────────────────────────────────┐
│             React + TypeScript Frontend (Vite)         │
│  - Score Gauges & Breakdown   - Job Description Matcher│
│  - ATS Audit Card             - 4-Phase Career Roadmap │
│  - Drag & Drop Uploader       - AI Resume Improver     │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP / REST APIs (JSON)
                            ▼
┌────────────────────────────────────────────────────────┐
│                 FastAPI Backend Engine                 │
│  - JWT Bearer Authentication & PBKDF2 Password Hashing │
│  - Document Ingestion & Validation Middleware          │
│  - RESTful API Routers (/resumes, /analysis, /roadmap) │
└─────────────┬──────────────────────────┬───────────────┘
              │                          │
              ▼                          ▼
┌───────────────────────────┐  ┌─────────────────────────┐
│     AI & NLP Pipeline     │  │     Data Persistence    │
│  - PyPDF / docx Parser    │  │  - PostgreSQL / SQLite  │
│  - Section Segmenter      │  │  - Relational Schema    │
│  - Skill Taxonomy (400+)  │  │  - JSON Analysis State  │
│  - TF-IDF Vectorizer      │  │  - Alembic Migrations   │
│  - 0-100 Scoring Engine   │  └─────────────────────────┘
│  - 8-Point ATS Checker    │
│  - Career Recommender     │
│  - AI Section Improver    │
└───────────────────────────┘
```

---

## 2. Component Design & Responsibilities

### 2.1 Presentation Layer (Frontend)
- **Framework**: React 18 with TypeScript and Vite for near-instant HMR.
- **Styling**: Tailwind CSS with custom slate/indigo aesthetic and modern dark mode typography.
- **Visualization**: Recharts for category bar charts, skill distribution histograms, and animated SVG circular gauges.
- **Client Routing**: React Router v6 with clean separation across Dashboard, Document Upload, Audit Details, Job Matcher, Career Roadmap, and AI Enhancer.
- **Resilience**: Integrated with an automatic fallback mock data layer to allow seamless visual previews even when offline.

### 2.2 Application Services Layer (Backend)
- **Framework**: FastAPI (Python 3.11), taking advantage of asynchronous request processing and automatic OpenAPI/Swagger generation.
- **Security & Authorization**: PBKDF2-HMAC-SHA256 password salting, HS256 JWT tokens with 7-day expiration, and XSS/HTML tag sanitization.
- **File Ingestion**: 15MB file size limits, MIME type validation, and extension verification.

### 2.3 AI / NLP Pipeline Layer
1. **Document Parser (`ResumeParserService`)**: Multi-tiered parsing for native PDF (`pypdf`, `pdfplumber`), Microsoft Word (`python-docx`), plain text, and OCR fallback (`pytesseract`).
2. **Text Normalization & Section Segmenter (`text_cleaning`)**: Unicode normalization, bullet point extraction, and regular expression boundary matching across 10 standard resume sections.
3. **Skill Taxonomy (`SkillsTaxonomyService`)**: 400+ indexed technical and soft skills categorized into 10 domains (Programming Languages, Frameworks, Cloud & DevOps, Databases, ML/AI, Data Engineering, Web Tech, Soft Skills, Tools, Cybersecurity).
4. **Entity Extraction (`NLPExtractorService`)**: Heuristic and regular expression extractors for names, phone numbers, email addresses, GitHub/LinkedIn links, university degrees, graduation years, GPA, and work history.
5. **Scoring Engine (`ScoringEngineService`)**: 5-factor explainable 0-100 scoring model with strengths and weaknesses generation.
6. **ATS Audit Engine (`AtsAnalyzerService`)**: Evaluates 8 mission-critical applicant tracking system factors (format, text readability, contact completeness, standard headers, tables, length, keyword density, and skill visibility).
7. **Semantic Matcher (`SemanticMatcherService`)**: TF-IDF cosine similarity, n-gram tokenization, and Jaccard skill set comparisons.
8. **Career Recommender (`CareerRecommenderService`)**: Matches extracted profile against 12 industry job roles with weighted skill calculation.
9. **Resume Improver (`ResumeImproverService`)**: Section rewriter utilizing Google's XYZ formula (`Accomplished [X] as measured by [Y], by doing [Z]`), injecting power verbs and quantifiable metrics.
10. **Roadmap Generator (`RoadmapGeneratorService`)**: 4-phase, 24-week personal development roadmap targeting identified skill gaps.

---

## 3. Database Schema

The database utilizes relational integrity with foreign key cascades:
- **`users`**: Authentication table with hashed credentials and profile metadata.
- **`resumes`**: Stored resume records, file paths, versions, and extracted raw text.
- **`analyses`**: Full evaluation records containing overall scores, ATS ratings, category breakdown JSON, strengths/weaknesses JSON, and ATS audit details.
- **`job_roles`**: Catalog of 12 benchmark tech roles with required/optional skills, weights, certifications, and project templates.
- **`job_matches`**: Historical matches between specific resumes and job postings.
- **`roadmaps`**: Generated 4-phase career roadmaps.
