import json
from fastapi import APIRouter, HTTPException, Depends
from app.api.deps import get_current_user
from app.core.database import get_db_connection
from app.schemas.analysis import ResumeImprovementRequest, ResumeImprovementResponse
from app.services.resume_improver import ResumeImproverService

router = APIRouter(prefix="/analysis", tags=["Resume Improvement Assistant"])

@router.post("/{resume_id}/improve-section", response_model=ResumeImprovementResponse)
def improve_resume_section(
    resume_id: str,
    req: ResumeImprovementRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT parsed_data FROM analyses WHERE resume_id = ? AND user_id = ? ORDER BY created_at DESC LIMIT 1", (resume_id, current_user["id"]))
    row = cursor.fetchone()
    conn.close()
    
    parsed_dict = json.loads(row["parsed_data"]) if row else None
    
    improved = ResumeImproverService.improve_section(
        section=req.section,
        content=req.content,
        target_role=req.target_role,
        parsed_data=parsed_dict
    )
    return improved
