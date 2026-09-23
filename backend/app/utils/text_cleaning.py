import re
import unicodedata
from typing import Dict, List, Tuple

SECTION_KEYWORDS = {
    "summary": [
        "summary", "professional summary", "career objective", "objective",
        "about me", "profile", "executive summary", "personal summary"
    ],
    "experience": [
        "experience", "work experience", "professional experience", "employment history",
        "work history", "internship experience", "internships", "relevant experience"
    ],
    "education": [
        "education", "academic background", "academic history", "educational qualifications",
        "qualifications", "academics"
    ],
    "skills": [
        "skills", "technical skills", "core competencies", "skills & competencies",
        "technologies", "tech stack", "tools & technologies", "technical proficiencies",
        "areas of expertise", "programming skills"
    ],
    "projects": [
        "projects", "academic projects", "personal projects", "key projects",
        "technical projects", "notable projects", "open source contributions"
    ],
    "certifications": [
        "certifications", "certificates", "licenses & certifications", "credentials",
        "professional certifications", "accreditations", "courses & certifications"
    ],
    "awards": [
        "awards", "honors", "achievements", "accomplishments", "recognition"
    ],
    "languages": [
        "languages", "languages known"
    ]
}

def clean_text(text: str) -> str:
    """Normalize whitespace, remove invalid Unicode characters, standardize quotes and dashes."""
    if not text:
        return ""
    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)
    # Replace smart quotes and dashes
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    text = text.replace("—", "-").replace("–", "-").replace("•", "\n• ").replace("·", "\n• ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Clean multiple spaces while preserving newlines
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    cleaned = "\n".join(lines)
    # Clean excessive blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()

def segment_sections(raw_text: str) -> Dict[str, str]:
    """Segment resume text into standard sections based on identified headers."""
    cleaned = clean_text(raw_text)
    lines = cleaned.split("\n")
    
    sections: Dict[str, List[str]] = {
        "header": [],
        "summary": [],
        "experience": [],
        "education": [],
        "skills": [],
        "projects": [],
        "certifications": [],
        "awards": [],
        "languages": [],
        "other": []
    }
    
    current_section = "header"
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
            
        # Check if this line is a section heading
        # A heading is typically short (< 45 chars) and matches one of the keywords
        norm_line = re.sub(r"[^a-zA-Z\s&]", "", line_stripped).strip().lower()
        matched_section = None
        
        if len(norm_line) < 45:
            for sec_name, keywords in SECTION_KEYWORDS.items():
                if norm_line in keywords or any(norm_line == kw for kw in keywords):
                    matched_section = sec_name
                    break
                    
        if matched_section:
            current_section = matched_section
        else:
            sections[current_section].append(line_stripped)
            
    # Combine lines into text
    result = {k: "\n".join(v).strip() for k, v in sections.items() if v}
    return result
