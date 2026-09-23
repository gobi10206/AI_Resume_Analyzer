import re
from typing import Dict, List, Any
from app.schemas.resume import ParsedResumeData
from app.schemas.analysis import (
    CategoryScore, ScoreBreakdown, StrengthWeaknessItem
)

ACTION_VERBS = {
    "architected", "developed", "engineered", "designed", "implemented", "optimized",
    "scaled", "spearheaded", "accelerated", "automated", "orchestrated", "reduced",
    "increased", "enhanced", "built", "created", "deployed", "launched", "managed",
    "led", "directed", "formulated", "established", "streamlined", "delivered"
}

class ScoringEngineService:
    @staticmethod
    def evaluate(parsed: ParsedResumeData, raw_text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates an explainable 0-100 overall score, category scores,
        strengths, and weaknesses.
        """
        strengths: List[StrengthWeaknessItem] = []
        weaknesses: List[StrengthWeaknessItem] = []
        
        # 1. Contact & Completeness (Max: 15)
        contact_score = 0.0
        contact_feedback = []
        info = parsed.personal_info
        
        if info.email:
            contact_score += 3.0
        else:
            contact_feedback.append("Missing contact email.")
            weaknesses.append(StrengthWeaknessItem(
                title="Missing Email Address",
                description="A professional email is fundamental for recruiter outreach.",
                impact="High",
                actionable_tip="Add a professional email (e.g., firstname.lastname@gmail.com) prominently in the header."
            ))
            
        if info.phone:
            contact_score += 3.0
        else:
            contact_feedback.append("Missing contact phone number.")
            weaknesses.append(StrengthWeaknessItem(
                title="Missing Phone Number",
                description="Recruiters often schedule screenings via phone/SMS.",
                impact="Medium",
                actionable_tip="Include your standard mobile number with international country code."
            ))
            
        if info.location:
            contact_score += 2.0
            
        if info.linkedin or info.github or info.portfolio:
            contact_score += 4.0
            strengths.append(StrengthWeaknessItem(
                title="Online Technical Presence",
                description="Your resume includes links to professional profiles (GitHub/LinkedIn), allowing recruiters to inspect real code and experience.",
                impact="High",
                actionable_tip="Keep your GitHub repositories well-documented with clear READMEs and live demo links."
            ))
        else:
            contact_feedback.append("No LinkedIn or GitHub profile link found.")
            weaknesses.append(StrengthWeaknessItem(
                title="Missing Technical Portfolio / GitHub",
                description="Engineering recruiters look for portfolio or GitHub links to verify hands-on coding capability.",
                impact="Medium",
                actionable_tip="Add your customized LinkedIn URL and GitHub profile to the top header."
            ))
            
        if parsed.summary:
            contact_score += 3.0
            strengths.append(StrengthWeaknessItem(
                title="Professional Summary Included",
                description="An opening summary provides immediate context on your career level, core competencies, and career trajectory.",
                impact="Medium",
                actionable_tip="Ensure your summary emphasizes your unique value proposition in 2-3 concise sentences."
            ))
        else:
            contact_feedback.append("Consider adding a 2-sentence career summary.")
            
        cat_contact = CategoryScore(
            category="Contact & Completeness",
            score=round(contact_score, 1),
            max_score=15.0,
            percentage=round((contact_score / 15.0) * 100, 1),
            feedback="; ".join(contact_feedback) if contact_feedback else "Contact information is complete and well-structured."
        )

        # 2. Experience & Impact (Max: 25)
        exp_score = 0.0
        exp_feedback = []
        metric_regex = re.compile(r"\b(\d+[\d,.]*\%|\$\d+[\d,.]*|\d+x|\d+\+?\s*(?:users|clients|ms|seconds|minutes|hours|queries|requests|pipelines))\b", re.IGNORECASE)
        
        num_exp = len(parsed.experience)
        if num_exp >= 2:
            exp_score += 10.0
        elif num_exp == 1:
            exp_score += 6.0
        else:
            exp_feedback.append("No professional work experience or internships detected.")
            weaknesses.append(StrengthWeaknessItem(
                title="Limited Work Experience",
                description="Resumes without distinct internship or work experience struggle with senior or mid-level filters.",
                impact="High",
                actionable_tip="If you are a student or recent graduate, detail your academic internships, freelancing, or open-source roles under Experience."
            ))
            
        # Analyze bullet points and metrics
        all_bullets = []
        for exp in parsed.experience:
            all_bullets.extend(exp.bullet_points)
            
        if len(all_bullets) >= 4:
            exp_score += 5.0
        elif len(all_bullets) >= 2:
            exp_score += 3.0
            
        # Metric count
        metrics_found = [b for b in all_bullets if metric_regex.search(b)]
        if len(metrics_found) >= 3:
            exp_score += 6.0
            strengths.append(StrengthWeaknessItem(
                title="Strong Metric-Driven Achievements",
                description=f"Identified {len(metrics_found)} bullet points with quantifiable metrics and measurable business outcomes.",
                impact="High",
                actionable_tip="Continue using Google's X-Y-Z formula: 'Accomplished [X] as measured by [Y], by doing [Z]'."
            ))
        elif len(metrics_found) >= 1:
            exp_score += 3.0
        else:
            exp_feedback.append("Bullets lack quantifiable metrics (percentages, dollar amounts, scale).")
            weaknesses.append(StrengthWeaknessItem(
                title="Lack of Quantifiable Results",
                description="Your experience descriptions focus on responsibilities rather than measurable business impact.",
                impact="High",
                actionable_tip="Add specific numbers (e.g., 'reduced API latency by 35%', 'automated 12 CI/CD steps', 'scaled to 10k users')."
            ))
            
        # Action verbs
        action_verb_count = sum(1 for b in all_bullets if any(b.lower().startswith(av) or f" {av} " in b.lower() for av in ACTION_VERBS))
        if action_verb_count >= 3:
            exp_score += 4.0
        else:
            exp_score += 2.0
            exp_feedback.append("Use stronger active verbs at the start of bullet points.")

        cat_exp = CategoryScore(
            category="Experience & Impact",
            score=round(exp_score, 1),
            max_score=25.0,
            percentage=round((exp_score / 25.0) * 100, 1),
            feedback="; ".join(exp_feedback) if exp_feedback else "Solid work experience with active phrasing and accomplishments."
        )

        # 3. Skills & Relevance (Max: 25)
        skills_score = 0.0
        skills_feedback = []
        skill_count = len(parsed.skills)
        cat_count = len(parsed.categorized_skills)
        
        if skill_count >= 15:
            skills_score += 15.0
            strengths.append(StrengthWeaknessItem(
                title="Extensive Technical Skill Inventory",
                description=f"Extracted {skill_count} relevant technical and domain skills across modern technology stacks.",
                impact="High",
                actionable_tip="Ensure all listed skills are backed up by concrete usage in your projects or work experience."
            ))
        elif skill_count >= 10:
            skills_score += 12.0
        elif skill_count >= 5:
            skills_score += 8.0
        else:
            skills_score += 4.0
            weaknesses.append(StrengthWeaknessItem(
                title="Low Skill Keyword Density",
                description=f"Only {skill_count} technical skills were recognized. ATS filters search for specific keyword proficiencies.",
                impact="High",
                actionable_tip="Add a dedicated Technical Skills section grouping languages, frameworks, databases, and developer tools."
            ))
            
        if cat_count >= 4:
            skills_score += 10.0
        elif cat_count >= 2:
            skills_score += 6.0
        else:
            skills_score += 3.0
            skills_feedback.append("Broaden your skill categories (include Cloud, DevOps, Testing, or Databases).")

        cat_skills = CategoryScore(
            category="Skills & Relevance",
            score=round(skills_score, 1),
            max_score=25.0,
            percentage=round((skills_score / 25.0) * 100, 1),
            feedback="; ".join(skills_feedback) if skills_feedback else "Excellent technical depth and balanced skill distribution."
        )

        # 4. Education & Certifications (Max: 15)
        edu_score = 0.0
        edu_feedback = []
        
        if len(parsed.education) > 0:
            edu_score += 7.0
            edu = parsed.education[0]
            if edu.graduation_year:
                edu_score += 2.0
            if edu.gpa:
                edu_score += 2.0
                strengths.append(StrengthWeaknessItem(
                    title="Academic Performance Highlighted",
                    description=f"Clear academic credentials with GPA/performance ({edu.gpa}) showcased.",
                    impact="Medium",
                    actionable_tip="Keep academic honors and relevant coursework listed if graduating within the past 3 years."
                ))
        else:
            weaknesses.append(StrengthWeaknessItem(
                title="Missing Formal Education Section",
                description="Recruiters and automated screeners verify degree requirements first.",
                impact="High",
                actionable_tip="Clearly list your Degree, University name, and Graduation year."
            ))
            
        if len(parsed.certifications) > 0:
            edu_score += 4.0
            strengths.append(StrengthWeaknessItem(
                title="Industry Certifications Verified",
                description=f"Found {len(parsed.certifications)} accredited certifications, demonstrating ongoing professional development.",
                impact="Medium",
                actionable_tip="Keep certification verification IDs or credential URLs linked."
            ))
        else:
            edu_feedback.append("No cloud or professional certifications detected.")
            
        cat_edu = CategoryScore(
            category="Education & Certifications",
            score=round(edu_score, 1),
            max_score=15.0,
            percentage=round((edu_score / 15.0) * 100, 1),
            feedback="; ".join(edu_feedback) if edu_feedback else "Clear academic credentials and verified qualifications."
        )

        # 5. Formatting & Structure (Max: 20)
        fmt_score = 0.0
        fmt_feedback = []
        word_count = metadata.get("word_count", 0)
        
        # Word count sweet spot: 350 to 950 words
        if 350 <= word_count <= 950:
            fmt_score += 7.0
            strengths.append(StrengthWeaknessItem(
                title="Optimal Document Length",
                description=f"Resume word count ({word_count} words) falls within the recommended 1 to 2 page industry standard.",
                impact="Low",
                actionable_tip="Maintain this concise density without adding filler fluff."
            ))
        elif word_count < 300:
            fmt_score += 3.0
            fmt_feedback.append(f"Resume is short ({word_count} words). Expand on project contributions and technical methodologies.")
        else:
            fmt_score += 4.0
            fmt_feedback.append(f"Resume is lengthy ({word_count} words). Consider trimming older or less relevant details.")
            
        # Section structure
        if len(parsed.experience) > 0 and len(parsed.education) > 0 and len(parsed.skills) > 0:
            fmt_score += 8.0
        else:
            fmt_score += 4.0
            
        # Clean parseability
        if not metadata.get("is_scanned", False):
            fmt_score += 5.0
        else:
            weaknesses.append(StrengthWeaknessItem(
                title="Scanned Image Document",
                description="Your document appears to be a scanned image PDF rather than selectable text, hindering ATS readability.",
                impact="High",
                actionable_tip="Export your resume directly from Word, Google Docs, or LaTeX as a text-native PDF."
            ))

        cat_fmt = CategoryScore(
            category="Formatting & Structure",
            score=round(fmt_score, 1),
            max_score=20.0,
            percentage=round((fmt_score / 20.0) * 100, 1),
            feedback="; ".join(fmt_feedback) if fmt_feedback else "Clean, standard structure optimal for recruitment parsers."
        )

        # Overall Score
        overall_score = round(contact_score + exp_score + skills_score + edu_score + fmt_score, 1)
        
        score_breakdown = ScoreBreakdown(
            contact_and_completeness=cat_contact,
            experience_and_impact=cat_exp,
            skills_and_relevance=cat_skills,
            education_and_certifications=cat_edu,
            formatting_and_structure=cat_fmt
        )
        
        return {
            "overall_score": overall_score,
            "score_breakdown": score_breakdown,
            "strengths": strengths,
            "weaknesses": weaknesses
        }
