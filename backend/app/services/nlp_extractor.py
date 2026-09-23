import re
from typing import Dict, List, Any, Optional, Tuple
from app.services.skills_taxonomy import skills_service
from app.schemas.resume import (
    ParsedResumeData, ParsedPersonalInfo, ParsedEducation,
    ParsedExperience, ParsedProject
)

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{10,13}")
LINKEDIN_REGEX = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/(?:in|pub)/[a-zA-Z0-9_-]+", re.IGNORECASE)
GITHUB_REGEX = re.compile(r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+", re.IGNORECASE)
PORTFOLIO_REGEX = re.compile(r"(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.(?:io|dev|me|tech|site|com|org)(?:/[a-zA-Z0-9_-]+)?", re.IGNORECASE)

DEGREE_PATTERNS = [
    r"\b(?:Bachelor|B\.?Tech|B\.?E\.?|B\.?S\.?|B\.?Sc|BCA)\b(?:\s+(?:of|in)\s+[A-Za-z\s]+)?",
    r"\b(?:Master|M\.?Tech|M\.?E\.?|M\.?S\.?|M\.?Sc|MCA|MBA)\b(?:\s+(?:of|in)\s+[A-Za-z\s]+)?",
    r"\b(?:Ph\.?D|Doctor of Philosophy)\b(?:\s+(?:in)\s+[A-Za-z\s]+)?",
    r"\b(?:Associate|Diploma)\b(?:\s+(?:of|in)\s+[A-Za-z\s]+)?"
]

GPA_REGEX = re.compile(r"\b(?:(?:GPA|CGPA|Score)[\s:]*([0-9]\.[0-9]{1,2}(?:\s*/\s*(?:4\.0|10\.0|4|10))?)|(?:([0-9]{1,2}(?:\.[0-9]{1,2})?)\s*(?:CGPA|GPA|%)))\b", re.IGNORECASE)
YEAR_REGEX = re.compile(r"\b(19[89]\d|20[0-3]\d)\b")
DATE_RANGE_REGEX = re.compile(
    r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|\d{4})\s*(?:-|–|to)\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|\d{4}|Present|Current)\b",
    re.IGNORECASE
)

JOB_TITLES_COMMON = [
    "software engineer", "full stack engineer", "full stack developer", "frontend developer",
    "backend developer", "data scientist", "machine learning engineer", "data analyst",
    "devops engineer", "cloud architect", "mobile developer", "android developer", "ios developer",
    "ai research engineer", "product manager", "qa engineer", "systems engineer",
    "intern", "software development intern", "research intern", "consultant"
]

class NLPExtractorService:
    @staticmethod
    def extract_entities(raw_text: str, sections: Dict[str, str], metadata: Dict[str, Any]) -> ParsedResumeData:
        personal_info = NLPExtractorService._extract_personal_info(raw_text, sections.get("header", ""))
        skills_data = skills_service.extract_skills(raw_text)
        education_items = NLPExtractorService._extract_education(sections.get("education", ""), raw_text)
        experience_items, exp_years = NLPExtractorService._extract_experience(sections.get("experience", ""), raw_text)
        project_items = NLPExtractorService._extract_projects(sections.get("projects", ""), raw_text)
        certifications = NLPExtractorService._extract_certifications(sections.get("certifications", ""), raw_text)
        summary_text = sections.get("summary", "")
        if not summary_text:
            header_lines = sections.get("header", "").split("\n")
            if len(header_lines) > 2 and len(" ".join(header_lines[2:])) > 60:
                summary_text = " ".join(header_lines[2:])
        languages = NLPExtractorService._extract_languages(sections.get("languages", ""), raw_text)
        
        return ParsedResumeData(
            personal_info=personal_info,
            summary=summary_text.strip() if summary_text else None,
            skills=skills_data["all_skills"],
            categorized_skills=skills_data["categorized"],
            education=education_items,
            experience=experience_items,
            projects=project_items,
            certifications=certifications,
            languages=languages,
            estimated_experience_years=exp_years
        )
        
    @staticmethod
    def _extract_personal_info(raw_text: str, header_text: str) -> ParsedPersonalInfo:
        search_zone = header_text if len(header_text) > 20 else raw_text[:1200]
        emails = EMAIL_REGEX.findall(search_zone)
        email = emails[0] if emails else None
        
        phones = PHONE_REGEX.findall(search_zone)
        phone = None
        for p in phones:
            digits_only = re.sub(r"\D", "", p)
            if len(digits_only) in [10, 11, 12, 13]:
                phone = p.strip()
                break
                
        linkedin = None
        gh = None
        li_match = LINKEDIN_REGEX.search(raw_text)
        if li_match:
            linkedin = li_match.group(0)
            if not linkedin.startswith("http"):
                linkedin = "https://" + linkedin
                
        gh_match = GITHUB_REGEX.search(raw_text)
        if gh_match:
            gh = gh_match.group(0)
            if not gh.startswith("http"):
                gh = "https://" + gh
                
        name = None
        lines = [line.strip() for line in search_zone.split("\n") if line.strip()]
        for line in lines[:5]:
            if "@" in line or "http" in line or "github" in line or "linkedin" in line:
                continue
            cleaned_line = re.sub(r"[^a-zA-Z\s]", "", line).strip()
            words = cleaned_line.split()
            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                lower_line = cleaned_line.lower()
                if not any(bad in lower_line for bad in ["resume", "curriculum", "vitae", "summary", "profile", "contact", "developer", "engineer"]):
                    name = cleaned_line
                    break
                    
        location = None
        loc_patterns = [
            r"([A-Z][a-zA-Z\s]+,\s*[A-Z]{2}\b)",
            r"([A-Z][a-zA-Z\s]+,\s*[A-Z][a-zA-Z\s]+)"
        ]
        for pat in loc_patterns:
            loc_m = re.search(pat, search_zone)
            if loc_m:
                cand = loc_m.group(1).strip()
                if not any(w in cand.lower() for w in ["university", "college", "school", "jan", "feb", "present", "gpa", "bachelor", "master"]):
                    location = cand
                    break

        return ParsedPersonalInfo(
            full_name=name,
            email=email,
            phone=phone,
            location=location,
            linkedin=linkedin,
            github=gh
        )
        
    @staticmethod
    def _extract_education(education_text: str, full_text: str) -> List[ParsedEducation]:
        text_to_search = education_text if len(education_text) > 30 else full_text
        items: List[ParsedEducation] = []
        lines = [l.strip() for l in text_to_search.split("\n") if l.strip()]
        current_degree = None
        current_inst = None
        current_year = None
        current_gpa = None
        
        for line in lines:
            for deg_pat in DEGREE_PATTERNS:
                deg_match = re.search(deg_pat, line, re.IGNORECASE)
                if deg_match:
                    current_degree = deg_match.group(0).strip()
                    break
            if any(kw in line.lower() for kw in ["university", "college", "institute", "school", "academy", "polytechnic"]):
                current_inst = line.strip()
            yr_match = YEAR_REGEX.findall(line)
            if yr_match:
                current_year = yr_match[-1]
            gpa_m = GPA_REGEX.search(line)
            if gpa_m:
                current_gpa = gpa_m.group(0).strip()
            if current_degree and (current_inst or current_year):
                items.append(ParsedEducation(
                    degree=current_degree,
                    institution=current_inst,
                    graduation_year=current_year,
                    gpa=current_gpa
                ))
                current_degree = None
                current_inst = None
                current_year = None
                current_gpa = None
        if not items and current_degree:
            items.append(ParsedEducation(
                degree=current_degree,
                institution=current_inst,
                graduation_year=current_year,
                gpa=current_gpa
            ))
        return items

    @staticmethod
    def _extract_experience(experience_text: str, full_text: str) -> Tuple[List[ParsedExperience], float]:
        text_to_search = experience_text if len(experience_text) > 40 else ""
        items: List[ParsedExperience] = []
        total_months = 0
        if not text_to_search:
            return items, 0.0
            
        blocks = re.split(r"\n(?=[A-Z][a-zA-Z\s]{3,40}(?:\s*[-|–]\s*|\s+at\s+|\s*\n))", text_to_search)
        for block in blocks:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if not lines:
                continue
            title = None
            company = None
            start_date = None
            end_date = None
            bullets = []
            date_m = DATE_RANGE_REGEX.search(block)
            if date_m:
                start_date = date_m.group(1).strip()
                end_date = date_m.group(2).strip()
            for line in lines[:3]:
                lower_line = line.lower()
                for jt in JOB_TITLES_COMMON:
                    if jt in lower_line:
                        title = line
                        break
                if title:
                    break
            if not title and len(lines) > 0:
                title = lines[0]
            for line in lines[:3]:
                if line != title and any(kw in line.lower() for kw in ["inc", "llc", "technologies", "solutions", "corp", "labs", "systems", "company", "pvt", "ltd"]):
                    company = line
                    break
            if not company and len(lines) > 1 and lines[1] != title:
                company = lines[1]
            for line in lines:
                if line.startswith("•") or line.startswith("-") or line.startswith("*"):
                    cleaned_bullet = re.sub(r"^[•\-\*]\s*", "", line).strip()
                    if len(cleaned_bullet) > 15:
                        bullets.append(cleaned_bullet)
                elif len(line) > 40 and line not in [title, company]:
                    bullets.append(line)
            items.append(ParsedExperience(
                job_title=title,
                company=company,
                start_date=start_date,
                end_date=end_date,
                bullet_points=bullets
            ))
            if start_date and end_date:
                total_months += 18
            else:
                total_months += 12
        estimated_years = round(total_months / 12.0, 1)
        return items, estimated_years

    @staticmethod
    def _extract_projects(projects_text: str, full_text: str) -> List[ParsedProject]:
        text_to_search = projects_text if len(projects_text) > 30 else ""
        items: List[ParsedProject] = []
        if not text_to_search:
            return items
        blocks = re.split(r"\n(?=[A-Z0-9][a-zA-Z0-9\s-]{2,40}(?:\s*\||\s*\(|\s*[-–:]))", text_to_search)
        for block in blocks:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if not lines:
                continue
            title_line = lines[0]
            desc_lines = lines[1:]
            tech_match = skills_service.extract_skills(block)
            technologies = tech_match["all_skills"]
            link = None
            url_match = re.search(r"https?://[^\s]+", block)
            if url_match:
                link = url_match.group(0)
            items.append(ParsedProject(
                title=title_line,
                description=" ".join(desc_lines) if desc_lines else title_line,
                technologies=technologies,
                link=link
            ))
        return items

    @staticmethod
    def _extract_certifications(cert_text: str, full_text: str) -> List[str]:
        text_to_search = cert_text if len(cert_text) > 20 else full_text
        certs: List[str] = []
        cert_keywords = [
            "AWS Certified", "Solutions Architect", "Developer Associate", "SysOps Administrator",
            "Azure Certified", "Google Cloud Certified", "Cloud Architect", "PMP", "CompTIA",
            "Certified Kubernetes Administrator", "CKA", "CKAD", "Cisco CCNA", "CCNP",
            "TensorFlow Developer", "Deep Learning Specialization", "Scrum Master", "CSM",
            "NPTEL", "IIT Madras", "Coursera", "Udacity"
        ]
        for kw in cert_keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text_to_search, re.IGNORECASE):
                certs.append(kw)
        if cert_text:
            lines = [re.sub(r"^[•\-\*]\s*", "", l).strip() for l in cert_text.split("\n") if l.strip()]
            for line in lines:
                if len(line) < 80 and line not in certs:
                    certs.append(line)
        return list(dict.fromkeys(certs))

    @staticmethod
    def _extract_languages(lang_text: str, full_text: str) -> List[str]:
        common_langs = ["English", "Spanish", "French", "German", "Mandarin", "Hindi", "Tamil", "Japanese", "Russian", "Arabic"]
        found = []
        target = lang_text if lang_text else full_text
        for l in common_langs:
            if re.search(rf"\b{l}\b", target, re.IGNORECASE):
                found.append(l)
        return found
