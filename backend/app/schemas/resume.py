from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ResumeUploadResponse(BaseModel):
    id: str
    file_name: str
    file_type: str
    file_size: int
    version: int
    created_at: str
    raw_text_preview: str

class ResumeListItem(BaseModel):
    id: str
    file_name: str
    file_type: str
    file_size: int
    version: int
    created_at: str
    has_analysis: bool

class ParsedEducation(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    field_of_study: Optional[str] = None
    graduation_year: Optional[str] = None
    gpa: Optional[str] = None

class ParsedExperience(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_months: Optional[int] = None
    bullet_points: List[str] = []

class ParsedProject(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = []
    link: Optional[str] = None

class ParsedPersonalInfo(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

class ParsedResumeData(BaseModel):
    personal_info: ParsedPersonalInfo = ParsedPersonalInfo()
    summary: Optional[str] = None
    skills: List[str] = []
    categorized_skills: Dict[str, List[str]] = {}
    education: List[ParsedEducation] = []
    experience: List[ParsedExperience] = []
    projects: List[ParsedProject] = []
    certifications: List[str] = []
    languages: List[str] = []
    estimated_experience_years: float = 0.0
