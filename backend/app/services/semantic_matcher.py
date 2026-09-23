import re
import math
from typing import List, Dict, Set, Tuple, Any
import numpy as np

class SemanticMatcherService:
    @staticmethod
    def tokenize_and_clean(text: str) -> List[str]:
        """Convert text to lowercase tokens, removing punctuation and common stop words."""
        STOP_WORDS = {
            "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
            "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were",
            "will", "with", "or", "this", "our", "their", "we", "you", "your", "can",
            "all", "any", "been", "have", "had", "than", "more", "also", "into", "over"
        }
        tokens = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
        return [t for t in tokens if t not in STOP_WORDS]

    @staticmethod
    def compute_cosine_similarity(text1: str, text2: str) -> float:
        """
        Compute TF-IDF cosine similarity between two texts.
        Uses pure numpy/math for robust zero-dependency execution.
        """
        tokens1 = SemanticMatcherService.tokenize_and_clean(text1)
        tokens2 = SemanticMatcherService.tokenize_and_clean(text2)
        
        if not tokens1 or not tokens2:
            return 0.0
            
        # Build vocabulary
        vocab = list(set(tokens1 + tokens2))
        vocab_index = {word: i for i, word in enumerate(vocab)}
        
        # Term frequencies
        tf1 = np.zeros(len(vocab))
        tf2 = np.zeros(len(vocab))
        
        for t in tokens1:
            tf1[vocab_index[t]] += 1
        for t in tokens2:
            tf2[vocab_index[t]] += 1
            
        # IDF calculation
        doc_count = 2
        idf = np.zeros(len(vocab))
        for word, i in vocab_index.items():
            df = (1 if tf1[i] > 0 else 0) + (1 if tf2[i] > 0 else 0)
            idf[i] = math.log((1 + doc_count) / (1 + df)) + 1.0
            
        # TF-IDF vectors
        tfidf1 = tf1 * idf
        tfidf2 = tf2 * idf
        
        # Cosine similarity
        norm1 = np.linalg.norm(tfidf1)
        norm2 = np.linalg.norm(tfidf2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return float(np.dot(tfidf1, tfidf2) / (norm1 * norm2))

    @staticmethod
    def compute_jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
        """Compute Jaccard similarity index between two sets."""
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return float(intersection / union) if union > 0 else 0.0

    @staticmethod
    def match_resume_to_jd(resume_text: str, resume_skills: List[str], jd_text: str) -> Dict[str, Any]:
        """
        Comprehensive comparison of a resume against a target job description:
        - Semantic cosine similarity
        - Skill extraction from JD and match %
        - Matching and missing skills
        - Keyword gaps
        - Actionable recommendations
        """
        from app.services.skills_taxonomy import skills_service
        
        # Extract skills from JD
        jd_skills_res = skills_service.extract_skills(jd_text)
        jd_skills = jd_skills_res["all_skills"]
        
        resume_skills_set = set(s.lower() for s in resume_skills)
        matching_skills = []
        missing_skills = []
        
        for skill in jd_skills:
            if skill.lower() in resume_skills_set:
                matching_skills.append(skill)
            else:
                missing_skills.append(skill)
                
        total_jd_skills = len(jd_skills)
        skill_match_pct = round((len(matching_skills) / total_jd_skills * 100), 1) if total_jd_skills > 0 else 75.0
        
        # Semantic text similarity
        semantic_sim = SemanticMatcherService.compute_cosine_similarity(resume_text, jd_text)
        semantic_sim_pct = round(semantic_sim * 100, 1)
        
        # Blended overall match (60% skill match + 40% semantic text overlap)
        overall_match = round((skill_match_pct * 0.6) + (min(100.0, semantic_sim_pct * 1.5) * 0.4), 1)
        overall_match = max(10.0, min(98.0, overall_match))
        
        # Keyword gaps: top words in JD not found in resume
        jd_tokens = set(SemanticMatcherService.tokenize_and_clean(jd_text))
        resume_tokens = set(SemanticMatcherService.tokenize_and_clean(resume_text))
        keyword_gaps = [w for w in (jd_tokens - resume_tokens) if len(w) > 4][:12]
        
        # Recommendations
        recommendations = []
        if missing_skills:
            top_missing = ", ".join(missing_skills[:5])
            recommendations.append(f"Incorporate missing core skills mentioned in the job description: {top_missing}.")
        if semantic_sim_pct < 45.0:
            recommendations.append("Align your experience bullet points with the specific domain terminology and responsibilities outlined in the job description.")
        if len(keyword_gaps) > 5:
            recommendations.append(f"Consider integrating relevant industry terms such as: {', '.join(keyword_gaps[:4])}.")
        if skill_match_pct >= 75.0:
            recommendations.append("Strong technical alignment. Highlight specific achievements, quantifiable metrics, and business outcomes for matching skills.")
            
        verdict = "Strong Match" if overall_match >= 75 else ("Moderate Match" if overall_match >= 55 else "Low Match")
        
        return {
            "overall_match_percentage": overall_match,
            "semantic_similarity": semantic_sim_pct,
            "skill_match_percentage": skill_match_pct,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "keyword_gaps": keyword_gaps,
            "ats_compatibility_verdict": verdict,
            "recommendations": recommendations
        }
