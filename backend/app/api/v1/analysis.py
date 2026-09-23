import json
from fastapi import APIRouter, HTTPException, Depends
from app.api.deps import get_current_user
from app.core.database import get_db_connection
from app.schemas.analysis import AnalysisResponse

router = APIRouter(prefix="/analysis", tags=["Resume Analysis"])

@router.get("/{resume_id}", response_model=AnalysisResponse)
def get_analysis_by_resume_id(resume_id: str, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM analyses
    WHERE resume_id = ? AND user_id = ?
    ORDER BY created_at DESC LIMIT 1
    """, (resume_id, current_user["id"]))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="No analysis found for this resume. Please upload or analyze first.")
        
    parsed_data = json.loads(row["parsed_data"])
    score_breakdown = json.loads(row["score_breakdown"])
    strengths = json.loads(row["strengths"])
    weaknesses = json.loads(row["weaknesses"])
    ats_report = json.loads(row["ats_report"])
    extracted_skills = json.loads(row["extracted_skills"])
    
    return AnalysisResponse(
        id=row["id"],
        resume_id=row["resume_id"],
        overall_score=row["overall_score"],
        ats_score=row["ats_score"],
        score_breakdown=score_breakdown,
        strengths=strengths,
        weaknesses=weaknesses,
        ats_report=ats_report,
        parsed_data=parsed_data,
        extracted_skills_count=len(extracted_skills),
        created_at=str(row["created_at"])
    )
