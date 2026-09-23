import json
from fastapi import APIRouter, HTTPException, Depends
from app.api.deps import get_current_user
from app.core.database import get_db_connection
from app.schemas.analysis import JobDescriptionMatchRequest, JobDescriptionMatchResponse
from app.services.semantic_matcher import SemanticMatcherService

router = APIRouter(prefix="/analysis", tags=["Job Description Matching"])

@router.post("/{resume_id}/match-jd", response_model=JobDescriptionMatchResponse)
def match_resume_with_job_description(
    resume_id: str,
    req: JobDescriptionMatchRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT raw_text FROM resumes WHERE id = ? AND user_id = ?", (resume_id, current_user["id"]))
    resume_row = cursor.fetchone()
    
    cursor.execute("SELECT extracted_skills FROM analyses WHERE resume_id = ? AND user_id = ? ORDER BY created_at DESC LIMIT 1", (resume_id, current_user["id"]))
    analysis_row = cursor.fetchone()
    conn.close()
    
    if not resume_row or not analysis_row:
        raise HTTPException(status_code=404, detail="Resume or analysis not found.")
        
    raw_text = resume_row["raw_text"] or ""
    skills = json.loads(analysis_row["extracted_skills"])
    
    match_result = SemanticMatcherService.match_resume_to_jd(raw_text, skills, req.job_description)
    
    return JobDescriptionMatchResponse(
        overall_match_percentage=match_result["overall_match_percentage"],
        semantic_similarity=match_result["semantic_similarity"],
        skill_match_percentage=match_result["skill_match_percentage"],
        matching_skills=match_result["matching_skills"],
        missing_skills=match_result["missing_skills"],
        qualification_gap="B.S. or B.Tech in Computer Science / AI / related fields verified" if "degree" in raw_text.lower() or "bachelor" in raw_text.lower() else "Ensure required academic qualifications are explicitly stated",
        experience_gap=None,
        keyword_gaps=match_result["keyword_gaps"],
        ats_compatibility_verdict=match_result["ats_compatibility_verdict"],
        recommendations=match_result["recommendations"]
    )
