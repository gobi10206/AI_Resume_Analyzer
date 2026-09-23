from app.schemas.resume import ParsedResumeData
from app.services.career_recommender import CareerRecommenderService
from app.services.roadmap_generator import RoadmapGeneratorService

def test_career_recommendations_and_roadmap():
    parsed = ParsedResumeData(
        skills=["Python", "FastAPI", "React", "JavaScript", "TypeScript", "PostgreSQL", "Docker", "RESTful APIs", "Git"]
    )
    matches = CareerRecommenderService.recommend_roles(parsed, limit=3)
    assert len(matches) > 0
    top_role = matches[0]
    assert top_role.match_percentage > 50.0
    
    # Test Roadmap Generation
    roadmap = RoadmapGeneratorService.generate_roadmap(top_role.role_title, top_role)
    assert len(roadmap.phases) == 4
    assert roadmap.target_role == top_role.role_title
    assert len(roadmap.phases[0].milestones) >= 2
