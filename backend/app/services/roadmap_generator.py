from typing import Dict, List, Any
from app.schemas.analysis import (
    CareerRoadmapResponse, CareerRoadmapPhase, RoleMatchItem
)

class RoadmapGeneratorService:
    @staticmethod
    def generate_roadmap(target_role: str, match_item: RoleMatchItem) -> CareerRoadmapResponse:
        """
        Synthesize a structured 6-month, 4-phase personal career roadmap
        tailored to bridge the specific missing skills for the target role.
        """
        match_score = match_item.match_percentage
        missing_skills = match_item.missing_skills
        
        # Readiness level
        if match_score >= 80.0:
            readiness = "Role Ready - Targeted Interview Prep & Portfolio Polish"
            timeframe = "4 to 8 Weeks"
        elif match_score >= 60.0:
            readiness = "Fast-Track Upskilling - Bridge Core Technical Gaps"
            timeframe = "12 to 16 Weeks"
        else:
            readiness = "Foundational Transition - Structured Multidisciplinary Path"
            timeframe = "20 to 24 Weeks"
            
        # Group missing skills into phases
        chunk1 = missing_skills[:3] if missing_skills else ["Core Architectural Foundations"]
        chunk2 = missing_skills[3:6] if len(missing_skills) > 3 else ["Advanced Framework Implementation"]
        chunk3 = missing_skills[6:9] if len(missing_skills) > 6 else ["System Design & Production Scale"]
        
        phases = [
            CareerRoadmapPhase(
                phase_number=1,
                duration="Weeks 1-4",
                title="Foundational Mastery & Tooling",
                focus_skills=chunk1,
                milestones=[
                    f"Complete deep dive into foundational paradigms of {', '.join(chunk1)}",
                    "Build small reproducible CLI utility or baseline microservice",
                    "Configure local Docker development workflow and linting standards"
                ],
                recommended_courses=[
                    f"Comprehensive Guide to {chunk1[0] if chunk1 else 'Modern Software Architecture'}",
                    "Clean Code & Modern Design Patterns"
                ],
                recommended_projects=[
                    {
                        "name": "Foundational API & Data Engine",
                        "description": "Develop a lightweight service implementing clean architecture and unit tests.",
                        "tech_stack": chunk1
                    }
                ]
            ),
            CareerRoadmapPhase(
                phase_number=2,
                duration="Weeks 5-10",
                title="Core Engineering & Framework Specialization",
                focus_skills=chunk2,
                milestones=[
                    f"Implement real-world domain workflows utilizing {', '.join(chunk2)}",
                    "Integrate automated CI/CD deployment pipelines with GitHub Actions",
                    "Achieve >85% test coverage and implement structured error logging"
                ],
                recommended_courses=[
                    f"Production {target_role} Masterclass",
                    "Cloud Native Infrastructure & Distributed Systems"
                ],
                recommended_projects=[
                    {
                        "name": "Full-Stack Enterprise Service",
                        "description": f"Build an end-to-end multi-tenant application incorporating {', '.join(chunk2)}.",
                        "tech_stack": chunk2 + ["PostgreSQL", "Docker"]
                    }
                ]
            ),
            CareerRoadmapPhase(
                phase_number=3,
                duration="Weeks 11-16",
                title="Advanced Scale, Optimization & Capstone Build",
                focus_skills=chunk3,
                milestones=[
                    "Conduct load testing and optimize database query plans for sub-50ms latency",
                    "Deploy containerized microservices to cloud staging environment (AWS/GCP)",
                    "Implement observability stack with Prometheus metrics and health monitoring"
                ],
                recommended_courses=[
                    "Distributed Systems & Scalability at Scale",
                    "Cloud Security, OAuth2, and Zero-Trust Fundamentals"
                ],
                recommended_projects=[
                    {
                        "name": f"Production Capstone for {target_role}",
                        "description": "High-availability platform handling real-time data streaming and caching.",
                        "tech_stack": ["FastAPI", "Kubernetes", "Redis", "Terraform"]
                    }
                ]
            ),
            CareerRoadmapPhase(
                phase_number=4,
                duration="Weeks 17-20",
                title="Portfolio Optimization, Mock Interviews & Placement",
                focus_skills=["System Design", "Behavioral Leadership", "Live Coding"],
                milestones=[
                    "Publish 3 capstone projects to GitHub with comprehensive documentation, demo GIFs, and live deployment links",
                    "Update resume bullets with metric-driven impact and pass ATS benchmarks (>85)",
                    "Complete 10 system design mock interviews and 20 LeetCode Medium challenges"
                ],
                recommended_courses=[
                    "Grokking the System Design Interview",
                    "Behavioral Interviewing for Top Tech Companies"
                ],
                recommended_projects=[
                    {
                        "name": "Live Portfolio & Case Studies",
                        "description": "Interactive developer portfolio showcasing system architecture diagrams and benchmarks.",
                        "tech_stack": ["React", "TypeScript", "Tailwind CSS"]
                    }
                ]
            )
        ]
        
        portfolio_improvements = [
            "Provide live demo URLs hosted on Vercel/Render/Fly.io for each portfolio project",
            "Write technical case study blog posts explaining architectural trade-offs and performance tuning",
            "Include architecture diagrams (Mermaid.js or PlantUML) in GitHub project READMEs"
        ]
        
        return CareerRoadmapResponse(
            target_role=target_role,
            readiness_level=readiness,
            current_match_score=match_score,
            estimated_timeframe=timeframe,
            phases=phases,
            recommended_certifications=match_item.recommended_certifications,
            portfolio_improvements=portfolio_improvements
        )
