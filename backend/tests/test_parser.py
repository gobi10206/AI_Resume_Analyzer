import io
from app.services.parser import ResumeParserService
from app.utils.text_cleaning import clean_text, segment_sections

def test_clean_text():
    dirty = "John   Doe \r\n\r\n\r\n Software “Engineer” — Tech\n• Bullet 1"
    cleaned = clean_text(dirty)
    assert "“" not in cleaned
    assert '"Engineer"' in cleaned
    assert "John Doe" in cleaned

def test_segment_sections():
    text = """
    John Doe
    john@example.com

    SUMMARY
    Senior Engineer with 5 years experience.

    EXPERIENCE
    Software Engineer at TechCorp
    • Built web apps.

    EDUCATION
    BS in Computer Science, Stanford University

    SKILLS
    Python, React, Docker
    """
    sections = segment_sections(text)
    assert "summary" in sections
    assert "experience" in sections
    assert "education" in sections
    assert "skills" in sections
    assert "Python, React, Docker" in sections["skills"]

def test_parse_txt_file():
    content = b"Alex Smith\nalex@example.com\n\nEXPERIENCE\nDevOps Engineer\n"
    res = ResumeParserService.parse_file(content, "alex.txt")
    assert res["metadata"]["file_type"] == ".txt"
    assert "Alex Smith" in res["raw_text"]
    assert res["metadata"]["word_count"] >= 5
