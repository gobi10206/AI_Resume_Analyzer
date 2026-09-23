from app.schemas.resume import ParsedResumeData, ParsedPersonalInfo
from app.services.ats_analyzer import AtsAnalyzerService

def test_ats_analyzer_high_score():
    parsed = ParsedResumeData(
        personal_info=ParsedPersonalInfo(
            full_name="Mark Spencer",
            email="mark@example.com",
            phone="555-901-2345"
        ),
        skills=["Python", "Docker", "Kubernetes", "AWS", "Terraform", "PostgreSQL", "Go", "React"],
        categorized_skills={"backend": ["Python", "Go"], "cloud": ["AWS", "Docker", "Kubernetes"]}
    )
    metadata = {
        "file_type": ".pdf",
        "is_scanned": False,
        "word_count": 520,
        "has_tables": False
    }
    sections = {
        "experience": "Senior Engineer at CloudCorp...",
        "education": "BS in CS...",
        "skills": "Python, Docker, AWS..."
    }
    raw_text = "Mark Spencer mark@example.com 555-901-2345 Senior Engineer at CloudCorp..."
    
    report = AtsAnalyzerService.analyze(parsed, raw_text, metadata, sections)
    assert report.ats_score >= 80.0
    assert report.verdict == "Excellent ATS Compatibility"
    assert report.passed_checks_count >= 6
