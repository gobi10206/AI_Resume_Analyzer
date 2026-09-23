import os
import json
import re
from typing import Dict, List, Set, Tuple, Any

class SkillsTaxonomyService:
    def __init__(self):
        self.taxonomy: Dict[str, List[Dict]] = {}
        self.skill_to_category: Dict[str, str] = {}
        self.skill_lookup: Dict[str, str] = {}  # term.lower() -> canonical_name
        self.multi_word_terms: List[Tuple[str, str, re.Pattern]] = []
        self.single_word_terms: List[Tuple[str, str, re.Pattern]] = []
        self.load_taxonomy()
        
    def load_taxonomy(self):
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/skills_taxonomy.json"))
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                self.taxonomy = json.load(f)
        else:
            self.taxonomy = {}
            
        # Build search indexes
        for category, skills in self.taxonomy.items():
            for item in skills:
                name = item["name"]
                self.skill_to_category[name] = category
                
                # Canonical name itself
                self.skill_lookup[name.lower()] = name
                
                # Synonyms
                synonyms = item.get("synonyms", [])
                for syn in synonyms:
                    self.skill_lookup[syn.lower()] = name
                    
        # Compile regex patterns for fast, boundary-aware matching
        for term, canonical in self.skill_lookup.items():
            escaped = re.escape(term)
            
            # Special handling for single-character or short languages like C, R, Go
            if term in ["c", "r"]:
                pattern = re.compile(rf"(?:(?<=\s)|(?<=^)|(?<=[,\./;:])){escaped}(?=[,\./;:!\s\)]|$)", re.IGNORECASE)
            elif term == "go":
                pattern = re.compile(r"\b(?:golang|go\s+programming|go\s+language)\b|\bGo\b", re.IGNORECASE)
            else:
                pattern = re.compile(rf"\b{escaped}\b", re.IGNORECASE)
                
            if " " in term or "-" in term or "_" in term:
                self.multi_word_terms.append((term, canonical, pattern))
            else:
                self.single_word_terms.append((term, canonical, pattern))
                
        # Sort multi-word terms by length descending to match longest phrases first
        self.multi_word_terms.sort(key=lambda x: len(x[0]), reverse=True)

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """
        Extract technical and soft skills from resume text.
        Returns:
            - all_skills: list of canonical skill names (deduplicated)
            - categorized: dict of category_name -> list of skill names
            - skill_count: total count
        """
        if not text:
            return {"all_skills": [], "categorized": {}, "skill_count": 0}
            
        found_canonical: Set[str] = set()
        matched_spans: List[Tuple[int, int]] = []
        
        # 1. Match multi-word terms first (e.g. "Natural Language Processing", "Machine Learning", "Amazon Web Services")
        for term, canonical, pattern in self.multi_word_terms:
            for match in pattern.finditer(text):
                span = match.span()
                # Check overlap with existing matches
                if not any(s <= span[0] and span[1] <= e for s, e in matched_spans):
                    found_canonical.add(canonical)
                    matched_spans.append(span)
                    
        # 2. Match single-word terms (e.g. "Python", "Docker", "PostgreSQL", "React")
        for term, canonical, pattern in self.single_word_terms:
            for match in pattern.finditer(text):
                span = match.span()
                # Special filter for C/R: don't match if part of general words
                matched_text = match.group(0)
                if term in ["c", "r"] and not (matched_text.isupper() or "programming" in text.lower() or "languages" in text.lower()):
                    continue
                if not any(s <= span[0] and span[1] <= e for s, e in matched_spans):
                    found_canonical.add(canonical)
                    matched_spans.append(span)
                    
        # Categorize found skills
        categorized: Dict[str, List[str]] = {}
        for skill in sorted(found_canonical):
            cat = self.skill_to_category.get(skill, "other")
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(skill)
            
        return {
            "all_skills": sorted(list(found_canonical)),
            "categorized": categorized,
            "skill_count": len(found_canonical)
        }

# Global singleton
skills_service = SkillsTaxonomyService()
