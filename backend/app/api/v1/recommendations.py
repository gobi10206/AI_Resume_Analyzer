import json
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.api.deps import get_current_user
from app.core.database import get_db_connection
from app.schemas.resume import ParsedResumeData
from app.schemas.analysis import RoleMatchItem
from app.services.career_recommender import CareerRecommenderService

router = APIRouter(prefix="/analysis", tags=["Career Recommendations"])

@router.get("/{resume_id}/recommendations", response_model=List[RoleMatchItem])
def get_career_recommendations(resume_id: str, limit: int = 6, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT parsed_data FROM analyses WHERE resume_id = ? AND user_id = ? ORDER BY created_at DESC LIMIT 1", (resume_id, current_user["id"]))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found for this resume.")
        
    parsed_dict = json.loads(row["parsed_data"])
    parsed_obj = ParsedResumeData(**parsed_dict)
    
    recommendations = CareerRecommenderService.recommend_roles(parsed_obj, limit=limit)
    return recommendations
