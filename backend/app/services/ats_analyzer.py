import re
from typing import Dict, List, Any
from app.schemas.resume import ParsedResumeData
from app.schemas.analysis import AtsCheckItem, AtsReport

class AtsAnalyzerService:
    @staticmethod
    def analyze(parsed: ParsedResumeData, raw_text: str, metadata: Dict[str, Any], sections: Dict[str, str]) -> AtsReport:
        """
        Comprehensive ATS Compatibility Analysis:
        - Contact completeness
        - Standard section headers
        - File parseability & formatting
        - Tables & graphics risk
        - Word count and length
        - Keyword density & repetitive stuffing
        - Skill visibility
        """
        checks: List[AtsCheckItem] = []
        formatting_notes: List[str] = []
        score = 0.0
        
        # 1. File format check (Max: 10 pts)
        ext = metadata.get("file_type", "").lower()
        if ext in [".pdf", ".docx"]:
            score += 10.0
            checks.append(AtsCheckItem(
                check_name="File Format Compatibility",
                status="passed",
                details=f"File extension {ext.upper()} is widely accepted by 99% of enterprise ATS platforms (Workday, Greenhouse, Lever, Taleo)."
            ))
        else:
            score += 6.0
            checks.append(AtsCheckItem(
                check_name="File Format Compatibility",
                status="warning",
                details=f"File format {ext.upper()} is readable as text, but PDF or DOCX is preferred for formatting preservation.",
                recommendation="Convert to clean standard PDF or DOCX."
            ))
            
        # 2. Text Parseability / Scanned Check (Max: 15 pts)
        is_scanned = metadata.get("is_scanned", False)
        if not is_scanned and metadata.get("word_count", 0) > 100:
            score += 15.0
            checks.append(AtsCheckItem(
                check_name="Digital Text Readability",
                status="passed",
                details="Resume contains clean, selectable text and can be processed by automated regex and NLP parsers without OCR."
            ))
        else:
            checks.append(AtsCheckItem(
                check_name="Digital Text Readability",
                status="failed",
                details="Document text could not be directly selected or required OCR extraction, which can scramble resume fields in older ATS.",
                recommendation="Re-export your document directly from Google Docs, MS Word, or Overleaf as a text-native PDF."
            ))
            
        # 3. Contact Information (Max: 15 pts)
        has_email = bool(parsed.personal_info.email)
        has_phone = bool(parsed.personal_info.phone)
        if has_email and has_phone:
            score += 15.0
            checks.append(AtsCheckItem(
                check_name="Contact Information Completeness",
                status="passed",
                details=f"Email ({parsed.personal_info.email}) and phone ({parsed.personal_info.phone}) were successfully parsed."
            ))
        elif has_email or has_phone:
            score += 8.0
            checks.append(AtsCheckItem(
                check_name="Contact Information Completeness",
                status="warning",
                details="Either email or phone number is missing from the header.",
                recommendation="Ensure both email address and primary phone number are clearly stated."
            ))
        else:
            checks.append(AtsCheckItem(
                check_name="Contact Information Completeness",
                status="failed",
                details="Neither email nor phone number could be detected in the document header.",
                recommendation="Add contact information at the very top of your resume."
            ))
            
        # 4. Standard Section Headings (Max: 15 pts)
        found_sections = [s for s in ["experience", "education", "skills", "projects"] if s in sections and len(sections[s]) > 20]
        if len(found_sections) >= 3:
            score += 15.0
            checks.append(AtsCheckItem(
                check_name="Standard Section Headings",
                status="passed",
                details=f"Detected recognized standard section headings: {', '.join([s.title() for s in found_sections])}."
            ))
        elif len(found_sections) >= 2:
            score += 9.0
            checks.append(AtsCheckItem(
                check_name="Standard Section Headings",
                status="warning",
                details="Some standard section headers (like Experience or Skills) are missing or non-standard.",
                recommendation="Use universal headers: 'WORK EXPERIENCE', 'EDUCATION', 'TECHNICAL SKILLS', 'PROJECTS'."
            ))
        else:
            checks.append(AtsCheckItem(
                check_name="Standard Section Headings",
                status="failed",
                details="Unable to clearly delineate resume sections.",
                recommendation="Structure your resume with bold, standardized section headers on their own line."
            ))
            
        # 5. Tables & Graphics Check (Max: 10 pts)
        has_tables = metadata.get("has_tables", False)
        if not has_tables:
            score += 10.0
            checks.append(AtsCheckItem(
                check_name="Table & Multi-Column Layout Safety",
                status="passed",
                details="Document uses a single-column or linear layout without complex nested tables that can disrupt ATS reading order."
            ))
        else:
            score += 5.0
            checks.append(AtsCheckItem(
                check_name="Table & Multi-Column Layout Safety",
                status="warning",
                details="Detected tables or multi-column grid layouts. Some legacy ATS read across rows rather than down columns.",
                recommendation="Use simple tabbed margins or bullet points instead of HTML or Word table borders."
            ))
            formatting_notes.append("Detected table structure: Ensure important dates and job titles are on separate lines rather than adjacent cells.")
            
        # 6. Resume Word Count & Length (Max: 15 pts)
        wc = metadata.get("word_count", 0)
        if 350 <= wc <= 950:
            score += 15.0
            checks.append(AtsCheckItem(
                check_name="Resume Length & Word Count",
                status="passed",
                details=f"Word count is {wc} words (ideal 1-2 page range for mid and junior roles)."
            ))
        elif wc < 350:
            score += 8.0
            checks.append(AtsCheckItem(
                check_name="Resume Length & Word Count",
                status="warning",
                details=f"Word count is low ({wc} words). Recruiters look for sufficient context and achievements.",
                recommendation="Elaborate on project architecture, responsibilities, and specific tools used."
            ))
        else:
            score += 10.0
            checks.append(AtsCheckItem(
                check_name="Resume Length & Word Count",
                status="warning",
                details=f"Word count is high ({wc} words). If your experience is under 7 years, aim for under 900 words.",
                recommendation="Condense bullet points to focus exclusively on highest-impact accomplishments."
            ))
            
        # 7. Keyword Density & Stuffing Analysis (Max: 10 pts)
        words = re.findall(r"\b[a-zA-Z]{4,}\b", raw_text.lower())
        word_freq: Dict[str, int] = {}
        for w in words:
            word_freq[w] = word_freq.get(w, 0) + 1
            
        total_w = len(words)
        stuffed_words = [w for w, cnt in word_freq.items() if (cnt / total_w) > 0.045 and w not in ["experience", "software", "development", "project", "engineer"]]
        
        if not stuffed_words:
            score += 10.0
            checks.append(AtsCheckItem(
                check_name="Keyword Naturalness & Density",
                status="passed",
                details="Natural keyword distribution. No evidence of keyword stuffing or repetitive word repetition."
            ))
        else:
            score += 4.0
            checks.append(AtsCheckItem(
                check_name="Keyword Naturalness & Density",
                status="warning",
                details=f"High repetition detected for terms: {', '.join(stuffed_words[:3])}.",
                recommendation="Vary your vocabulary and avoid unnaturally repeating identical terms."
            ))
            
        # 8. Skill Visibility (Max: 10 pts)
        if len(parsed.skills) >= 8:
            score += 10.0
            checks.append(AtsCheckItem(
                check_name="Technical Skill Visibility",
                status="passed",
                details=f"Recognized {len(parsed.skills)} discrete technical competencies easily indexable by search bots."
            ))
        else:
            score += 5.0
            checks.append(AtsCheckItem(
                check_name="Technical Skill Visibility",
                status="warning",
                details="Fewer than 8 industry-standard skills were identified.",
                recommendation="Group your skills under clear categories: Programming Languages, Frameworks, Cloud, Databases."
            ))
            
        ats_score = round(min(100.0, score), 1)
        passed_count = sum(1 for c in checks if c.status == "passed")
        
        if ats_score >= 80.0:
            verdict = "Excellent ATS Compatibility"
        elif ats_score >= 65.0:
            verdict = "Moderate ATS Compatibility - Minor Optimizations Recommended"
        else:
            verdict = "Needs Structural ATS Optimization"
            
        return AtsReport(
            ats_score=ats_score,
            verdict=verdict,
            passed_checks_count=passed_count,
            total_checks_count=len(checks),
            checks=checks,
            formatting_notes=formatting_notes
        )
