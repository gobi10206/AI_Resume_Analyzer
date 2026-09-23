# AI Resume Analyzer - AI & NLP Pipeline Architecture

This document details the machine learning algorithms, natural language processing techniques, and scoring formulas powering the **AI Resume Analyzer**.

---

## 1. Document Extraction & Preprocessing

The ingestion pipeline handles heterogeneous document encodings:
- **PDF Extraction**: Employs `pypdf` stream processing with fallback to `pdfplumber` layout analysis. If character counts fall below 50 characters, scanned document detection activates OCR via `pytesseract`.
- **DOCX Extraction**: Traverses XML paragraph trees and table rows via `python-docx`.
- **Text Normalization**: Standardizes Unicode symbols (smart quotes, em dashes, non-breaking spaces) and formats bullet points (`•`, `*`, `-`).
- **Section Segmentation**: Regular expression boundary segmentation identifies 10 canonical resume sections:
  - Header / Contact Information
  - Professional Summary / Career Objective
  - Work Experience / Employment History
  - Education & Academic Credentials
  - Technical Skills & Core Competencies
  - Projects & Open Source Contributions
  - Certifications & Licenses
  - Awards & Honors
  - Languages Known

---

## 2. Skill Taxonomy & Ontology Extraction

The skill extraction engine references a comprehensive taxonomy of over 400 categorized competencies:
- **Taxonomy Categories**:
  1. `programming_languages` (Python, TypeScript, C++, Rust, Go, SQL, etc.)
  2. `frameworks` (FastAPI, React, Django, Next.js, PyTorch, etc.)
  3. `cloud_devops` (AWS, Docker, Kubernetes, Terraform, CI/CD, etc.)
  4. `databases` (PostgreSQL, Redis, MongoDB, Snowflake, etc.)
  5. `ml_ai` (Deep Learning, Transformers, MLOps, NLP, etc.)
  6. `data_engineering` (Kafka, Airflow, Spark, dbt, etc.)
  7. `web_technologies` (REST APIs, WebSockets, GraphQL, etc.)
  8. `soft_skills` (Problem Solving, Technical Communication, Leadership, etc.)
  9. `tools_and_platforms` (Git, Linux, Postman, Prometheus, etc.)
  10. `cybersecurity` (OAuth 2.0, OWASP, Penetration Testing, etc.)
- **Matching Algorithm**:
  - Multi-word phrases are evaluated first in descending length order (`Natural Language Processing`, `Amazon Web Services`) with span tracking to avoid duplicate matching.
  - Word boundary regex (`\b{skill}\b`) avoids false substring matches (e.g. preventing the word "skill" from matching "C" or "R").
  - Synonym resolution maps abbreviations (e.g., `AWS` -> `Amazon Web Services`, `k8s` -> `Kubernetes`).

---

## 3. Explainable 0-100 Scoring Model

The scoring engine evaluates five distinct categories:

$$\text{Overall Score} = S_{\text{contact}} + S_{\text{experience}} + S_{\text{skills}} + S_{\text{education}} + S_{\text{formatting}}$$

1. **Contact & Completeness ($S_{\text{contact}} \in [0, 15]$)**:
   - Email presence (+3 pts)
   - Phone number (+3 pts)
   - Location / Address (+2 pts)
   - GitHub / LinkedIn profile links (+4 pts)
   - Professional summary statement (+3 pts)
2. **Experience & Impact ($S_{\text{experience}} \in [0, 25]$)**:
   - Experience depth: 1 role (+6 pts), $\ge 2$ roles (+10 pts)
   - Bullet point volume ($\ge 4$ bullets = +5 pts)
   - Quantified metrics & measurable outcomes (percentages, dollar savings, multipliers = up to +6 pts)
   - High-impact action verbs (Architected, Engineered, Optimized = +4 pts)
3. **Skills & Relevance ($S_{\text{skills}} \in [0, 25]$)**:
   - Total skill count: $\ge 15$ skills (+15 pts), 10-14 skills (+12 pts), 5-9 skills (+8 pts)
   - Cross-domain diversity: $\ge 4$ distinct categories (+10 pts)
4. **Education & Certifications ($S_{\text{education}} \in [0, 15]$)**:
   - Verified Degree (+7 pts)
   - Graduation Year (+2 pts)
   - GPA / Academic Standing (+2 pts)
   - Accredited Industry Certifications (+4 pts)
5. **Formatting & Structure ($S_{\text{formatting}} \in [0, 20]$)**:
   - Standard section headings (+8 pts)
   - Optimal length: 350 to 950 words (+7 pts)
   - Native digital text parseability (+5 pts)

---

## 4. Semantic Matching & Vector Similarity

Matching against Job Descriptions combines two complementary models:
1. **TF-IDF Cosine Similarity**:
   $$\text{Cosine Sim}(d_1, d_2) = \frac{\vec{v_1} \cdot \vec{v_2}}{\|\vec{v_1}\| \|\vec{v_2}\|}$$
   Measures textual and domain vocabulary alignment between the candidate's resume and job requirements.
2. **Weighted Skill Overlap**:
   Evaluates required skills (weight 1.5) and optional skills (weight 1.0) against the candidate's verified skill set.
3. **Blended Score**:
   $$\text{Blended Match} = 0.6 \times \text{Skill Match \%} + 0.4 \times \min(100, 1.5 \times \text{Semantic Sim \%})$$

---

## 5. ATS Compatibility Audit Matrix

The ATS engine verifies 8 compliance parameters:
| Audit Check | Pass Criteria | Warning Criteria | Impact |
| :--- | :--- | :--- | :--- |
| **File Format** | `.pdf` or `.docx` | `.txt` | Formatting fidelity |
| **Text Readability** | Selectable Unicode text | Scanned image / OCR | Parser readability |
| **Contact Info** | Email & Phone found | Only one found | Recruiter outreach |
| **Section Headings** | $\ge 3$ standard headers | 2 standard headers | Parser categorization |
| **Table Layout** | Linear / No tables | Nested tables / Multi-col | Column reading order |
| **Resume Length** | 350 - 950 words | $<300$ or $>1000$ words | Screening fatigue |
| **Keyword Density** | Max term frequency $<4.5\%$ | Repetitive words $\ge 4.5\%$ | Keyword stuffing |
| **Skill Visibility** | $\ge 8$ categorized skills | $<8$ skills | Search query indexing |

---

## 6. AI Resume Improver & Google XYZ Formula

The AI rewrite assistant converts weak bullet points into high-impact accomplishments using Google's formula:

> **"Accomplished [X] as measured by [Y], by doing [Z]"**

- **Before**: "Worked on web backend and improved speed."
- **After**: "• Architected high-throughput REST APIs using FastAPI and PostgreSQL, reducing end-to-end response latency by 38% across 250,000+ daily transactions."
