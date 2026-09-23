from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.schemas.resume import ParsedResumeData

class CategoryScore(BaseModel):
    category: str
    score: float
    max_score: float
    percentage: float
    feedback: str

class ScoreBreakdown(BaseModel):
    contact_and_completeness: CategoryScore
    experience_and_impact: CategoryScore
    skills_and_relevance: CategoryScore
    education_and_certifications: CategoryScore
    formatting_and_structure: CategoryScore

class StrengthWeaknessItem(BaseModel):
    title: str
    description: str
    impact: str  # High, Medium, Low
    actionable_tip: str

class AtsCheckItem(BaseModel):
    check_name: str
    status: str  # passed, warning, failed
    details: str
    recommendation: Optional[str] = None

class AtsReport(BaseModel):
    ats_score: float
    verdict: str
    passed_checks_count: int
    total_checks_count: int
    checks: List[AtsCheckItem]
    formatting_notes: List[str]

class AnalysisResponse(BaseModel):
    id: str
    resume_id: str
    overall_score: float
    ats_score: float
    score_breakdown: ScoreBreakdown
    strengths: List[StrengthWeaknessItem]
    weaknesses: List[StrengthWeaknessItem]
    ats_report: AtsReport
    parsed_data: ParsedResumeData
    extracted_skills_count: int
    created_at: str

class JobDescriptionMatchRequest(BaseModel):
    job_description: str
    target_role: Optional[str] = None

class JobDescriptionMatchResponse(BaseModel):
    overall_match_percentage: float
    semantic_similarity: float
    skill_match_percentage: float
    matching_skills: List[str]
    missing_skills: List[str]
    qualification_gap: Optional[str] = None
    experience_gap: Optional[str] = None
    keyword_gaps: List[str]
    ats_compatibility_verdict: str
    recommendations: List[str]

class RoleMatchItem(BaseModel):
    role_id: str
    role_title: str
    department: str
    match_percentage: float
    matching_skills: List[str]
    missing_skills: List[str]
    skill_gap_percentage: float
    suggested_learning_path: List[Dict[str, Any]]
    recommended_projects: List[Dict[str, Any]]
    recommended_certifications: List[str]

class CareerRoadmapPhase(BaseModel):
    phase_number: int
    duration: str
    title: str
    focus_skills: List[str]
    milestones: List[str]
    recommended_courses: List[str]
    recommended_projects: List[Dict[str, Any]]

class CareerRoadmapResponse(BaseModel):
    target_role: str
    readiness_level: str
    current_match_score: float
    estimated_timeframe: str
    phases: List[CareerRoadmapPhase]
    recommended_certifications: List[str]
    portfolio_improvements: List[str]

class ResumeImprovementRequest(BaseModel):
    section: str  # "summary", "experience", "projects", "skills"
    content: Optional[str] = None
    target_role: Optional[str] = None

class ResumeImprovementResponse(BaseModel):
    section: str
    original_content: Optional[str] = None
    improved_content: str
    changes_made: List[str]
    key_metrics_added: List[str]
    power_words_used: List[str]
    ats_impact_summary: str
