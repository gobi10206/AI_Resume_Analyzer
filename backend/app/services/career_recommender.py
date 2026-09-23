import json
import os
from typing import List, Dict, Any
from app.core.database import get_db_connection
from app.schemas.resume import ParsedResumeData
from app.schemas.analysis import RoleMatchItem

class CareerRecommenderService:
    @staticmethod
    def get_all_roles() -> List[Dict[str, Any]]:
        roles = []
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM job_roles")
            rows = cursor.fetchall()
            for row in rows:
                r = dict(row)
                r["required_skills"] = json.loads(r["required_skills"])
                r["optional_skills"] = json.loads(r["optional_skills"])
                r["recommended_certifications"] = json.loads(r["recommended_certifications"]) if r.get("recommended_certifications") else []
                r["learning_path"] = json.loads(r["learning_path"]) if r.get("learning_path") else []
                r["sample_projects"] = json.loads(r["sample_projects"]) if r.get("sample_projects") else []
                roles.append(r)
            conn.close()
        except Exception:
            pass
            
        if not roles:
            json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/job_roles.json"))
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    roles = json.load(f)
        return roles

    @staticmethod
    def recommend_roles(parsed: ParsedResumeData, limit: int = 6) -> List[RoleMatchItem]:
        roles = CareerRecommenderService.get_all_roles()
        user_skills_set = set(s.lower() for s in parsed.skills)
        
        matches: List[RoleMatchItem] = []
        
        for r in roles:
            req_skills = r.get("required_skills", [])
            opt_skills = r.get("optional_skills", [])
            
            req_matched = []
            req_missing = []
            opt_matched = []
            opt_missing = []
            
            def check_skill_match(item):
                if isinstance(item, dict):
                    name = item.get("skill") or item.get("name") or str(item)
                    syns = item.get("synonyms", [])
                else:
                    name = str(item)
                    syns = []
                all_candidates = [name.lower()] + [s.lower() for s in syns]
                return name, any(c in user_skills_set for c in all_candidates)

            # Evaluate required skills
            for item in req_skills:
                name, matched = check_skill_match(item)
                if matched:
                    req_matched.append(name)
                else:
                    req_missing.append(name)
                    
            # Evaluate optional skills
            for item in opt_skills:
                name, matched = check_skill_match(item)
                if matched:
                    opt_matched.append(name)
                else:
                    opt_missing.append(name)
                    
            total_req = len(req_skills) or 1
            total_opt = len(opt_skills) or 1
            
            req_ratio = len(req_matched) / total_req
            opt_ratio = len(opt_matched) / total_opt
            
            # Weighted match: 75% required skills + 25% optional skills
            raw_score = (req_ratio * 0.75) + (opt_ratio * 0.25)
            match_pct = round(raw_score * 100, 1)
            gap_pct = round(max(0.0, 100.0 - match_pct), 1)
            
            lp = r.get("learning_path", [])
            if isinstance(lp, list) and lp and isinstance(lp[0], str):
                lp = [{"step": i + 1, "title": f"Milestone {i+1}", "description": desc} for i, desc in enumerate(lp)]
                
            projects = r.get("sample_projects", [])
            if isinstance(projects, list) and projects and isinstance(projects[0], str):
                projects = [{"title": p, "description": f"Hands-on project targeting {r.get('title')}", "tech_stack": []} for p in projects]
                
            certs = r.get("recommended_certifications", [])
            
            matches.append(RoleMatchItem(
                role_id=str(r.get("id", r.get("title"))),
                role_title=r.get("title", "Software Engineer"),
                department=r.get("department", "Engineering"),
                match_percentage=match_pct,
                matching_skills=req_matched + opt_matched,
                missing_skills=req_missing + opt_missing,
                skill_gap_percentage=gap_pct,
                suggested_learning_path=lp,
                recommended_projects=projects,
                recommended_certifications=certs
            ))
            
        matches.sort(key=lambda m: m.match_percentage, reverse=True)
        return matches[:limit]
