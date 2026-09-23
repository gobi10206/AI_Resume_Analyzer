from app.schemas.resume import ParsedResumeData, ParsedPersonalInfo, ParsedEducation, ParsedExperience
from app.services.scoring_engine import ScoringEngineService

def test_scoring_engine_full():
    parsed = ParsedResumeData(
        personal_info=ParsedPersonalInfo(
            full_name="Jane Developer",
            email="jane@example.com",
            phone="+1 555-123-4567",
            location="New York, NY",
            linkedin="https://linkedin.com/in/janedev",
            github="https://github.com/janedev"
        ),
        summary="Experienced Full Stack Developer with 4 years building scalable services.",
        skills=["Python", "FastAPI", "React", "Docker", "PostgreSQL", "AWS", "TypeScript", "Kubernetes", "Redis", "Git"],
        categorized_skills={
            "programming_languages": ["Python", "TypeScript"],
            "frameworks": ["FastAPI", "React"],
            "cloud_devops": ["AWS", "Docker", "Kubernetes"],
            "databases": ["PostgreSQL", "Redis"]
        },
        education=[
            ParsedEducation(degree="B.S. in Computer Science", institution="Columbia University", graduation_year="2020", gpa="3.9")
        ],
        experience=[
            ParsedExperience(
                job_title="Senior Software Engineer",
                company="FinTech Innovations",
                bullet_points=[
                    "Architected high-throughput payment microservice, reducing latency by 45%.",
                    "Deployed containerized services to AWS using Docker and Terraform.",
                    "Optimized PostgreSQL queries, cutting CPU load by 30%."
                ]
            ),
            ParsedExperience(
                job_title="Software Engineer",
                company="DataCore Labs",
                bullet_points=[
                    "Engineered RESTful APIs processing 150,000+ daily requests.",
                    "Automated CI/CD workflows with GitHub Actions."
                ]
            )
        ],
        certifications=["AWS Certified Solutions Architect"]
    )
    raw_text = "Jane Developer resume text with 400 words..."
    metadata = {"word_count": 450, "is_scanned": False, "file_type": ".pdf"}
    
    res = ScoringEngineService.evaluate(parsed, raw_text, metadata)
    
    assert 70.0 <= res["overall_score"] <= 100.0
    assert res["score_breakdown"].contact_and_completeness.score > 10.0
    assert res["score_breakdown"].experience_and_impact.score >= 15.0
    assert len(res["strengths"]) >= 2
