import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.api.deps import get_current_user
from app.core.database import get_db_connection
from app.schemas.resume import ParsedResumeData
from app.schemas.analysis import CareerRoadmapResponse
from app.services.career_recommender import CareerRecommenderService
from app.services.roadmap_generator import RoadmapGeneratorService

router = APIRouter(prefix="/analysis", tags=["Career Roadmap"])

class RoadmapRequest(BaseModel):
    target_role: Optional[str] = None

@router.post("/{resume_id}/roadmap", response_model=CareerRoadmapResponse)
def generate_career_roadmap(
    resume_id: str,
    req: RoadmapRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT parsed_data FROM analyses WHERE resume_id = ? AND user_id = ? ORDER BY created_at DESC LIMIT 1", (resume_id, current_user["id"]))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found for this resume.")
        
    parsed_dict = json.loads(row["parsed_data"])
    parsed_obj = ParsedResumeData(**parsed_dict)
    
    recommendations = CareerRecommenderService.recommend_roles(parsed_obj, limit=12)
    target_role_title = req.target_role or (recommendations[0].role_title if recommendations else "Full Stack Software Engineer")
    
    # Find matching RoleMatchItem
    selected_match = next((r for r in recommendations if r.role_title.lower() == target_role_title.lower()), None)
    if not selected_match and recommendations:
        selected_match = recommendations[0]
        
    roadmap = RoadmapGeneratorService.generate_roadmap(target_role_title, selected_match)
    return roadmap
