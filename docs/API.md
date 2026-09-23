# AI Resume Analyzer - REST API Specification

The API is served by default at `http://localhost:8000/api/v1` with interactive Swagger documentation available at `/docs` and ReDoc at `/redoc`.

---

## 1. Authentication Endpoints

### `POST /auth/register`
Creates a new candidate account.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "Jane Doe"
  }
  ```
- **Response** `200 OK`:
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "user": {
      "id": "uuid-v4",
      "email": "user@example.com",
      "full_name": "Jane Doe"
    }
  }
  ```

### `POST /auth/login`
Authenticates existing credentials.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```

### `GET /auth/me`
Fetches current authenticated profile (Requires `Authorization: Bearer <token>`).

---

## 2. Resume Management

### `POST /resumes/upload`
Uploads and processes a new resume file.
- **Content-Type**: `multipart/form-data`
- **Form Parameters**: `file` (PDF, DOCX, or TXT, max 15MB)
- **Response** `200 OK`:
  ```json
  {
    "id": "resume-uuid",
    "file_name": "resume.pdf",
    "file_type": ".pdf",
    "file_size": 142050,
    "version": 1,
    "created_at": "2026-09-22 14:30",
    "raw_text_preview": "Jane Doe..."
  }
  ```

### `GET /resumes`
Returns list of all resume versions uploaded by the authenticated user.

### `GET /resumes/{resume_id}`
Returns details for a specific resume record.

### `DELETE /resumes/{resume_id}`
Deletes resume file from storage and cleans up associated database analysis records.

---

## 3. Analysis & Evaluation

### `GET /analysis/{resume_id}`
Returns the comprehensive evaluation for a resume.
- **Response** `200 OK`:
  - `overall_score`: Float (0-100)
  - `ats_score`: Float (0-100)
  - `score_breakdown`: 5 category scores (Contact, Experience, Skills, Education, Formatting)
  - `strengths`: List of identified strengths with explanations and actionable tips
  - `weaknesses`: List of identified weaknesses with actionable remediation
  - `ats_report`: 8 automated checks with statuses (`passed`, `warning`, `failed`)
  - `parsed_data`: Structured personal info, education, experience, projects, skills

### `POST /analysis/{resume_id}/match-jd`
Compares the resume against an arbitrary job description text.
- **Request Body**:
  ```json
  {
    "job_description": "We are seeking a Senior DevOps Engineer...",
    "target_role": "DevOps Engineer"
  }
  ```
- **Response** `200 OK`:
  - `overall_match_percentage`: Float
  - `semantic_similarity`: Float
  - `skill_match_percentage`: Float
  - `matching_skills`: List[str]
  - `missing_skills`: List[str]
  - `keyword_gaps`: List[str]
  - `ats_compatibility_verdict`: String
  - `recommendations`: List[str]

### `GET /analysis/{resume_id}/recommendations`
Returns top matching industry job roles ranked by weighted fit percentage.

### `POST /analysis/{resume_id}/roadmap`
Generates a personalized 4-phase, 24-week career development roadmap.
- **Request Body**: `{"target_role": "Machine Learning Engineer"}`

### `POST /analysis/{resume_id}/improve-section`
Rewrites a resume section (Summary, Experience, Projects, Skills) using the Google XYZ formula and power verbs.
- **Request Body**:
  ```json
  {
    "section": "experience",
    "content": "• Worked on APIs and fixed bugs.",
    "target_role": "Full Stack Engineer"
  }
  ```
