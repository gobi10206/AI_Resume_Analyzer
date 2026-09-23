"""
AI & NLP Evaluation Suite
Evaluates precision, recall, and recommendation consistency across benchmark resumes.
"""
from app.services.skills_taxonomy import skills_service
from app.services.semantic_matcher import SemanticMatcherService
from app.services.career_recommender import CareerRecommenderService
from app.schemas.resume import ParsedResumeData

def test_skill_extraction_precision_and_recall():
    # Ground truth resume segment with known skills
    text = """
    Software Engineer with strong skills in Python, FastAPI, React.js, Docker,
    Amazon Web Services, PostgreSQL, and Kubernetes. Experienced in Natural Language Processing.
    """
    ground_truth_skills = {
        "Python", "FastAPI", "React", "Docker", "Amazon Web Services",
        "PostgreSQL", "Kubernetes", "Natural Language Processing"
    }
    
    extracted = set(skills_service.extract_skills(text)["all_skills"])
    
    # True positives, false positives, false negatives
    tp = len(extracted.intersection(ground_truth_skills))
    fp = len(extracted - ground_truth_skills)
    fn = len(ground_truth_skills - extracted)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    print(f"Skill Extraction Evaluation: Precision={precision:.2f}, Recall={recall:.2f}, F1={f1:.2f}")
    assert precision >= 0.85
    assert recall >= 0.85
    assert f1 >= 0.85

def test_recommendation_consistency_and_monotonicity():
    """
    Monotonicity Principle: Adding required skills for a role should strictly
    increase or preserve the match percentage for that role.
    """
    base_skills = ["Python", "SQL"]
    parsed_base = ParsedResumeData(skills=base_skills)
    recs_base = {r.role_title: r.match_percentage for r in CareerRecommenderService.recommend_roles(parsed_base, limit=12)}
    
    # Add Machine Learning specific skills
    ml_skills = base_skills + ["PyTorch", "TensorFlow", "Deep Learning", "Natural Language Processing", "Scikit-Learn"]
    parsed_ml = ParsedResumeData(skills=ml_skills)
    recs_ml = {r.role_title: r.match_percentage for r in CareerRecommenderService.recommend_roles(parsed_ml, limit=12)}
    
    # Check that Machine Learning Engineer match percentage strictly increased
    assert "Machine Learning Engineer" in recs_ml
    base_ml_score = recs_base.get("Machine Learning Engineer", 0)
    enhanced_ml_score = recs_ml["Machine Learning Engineer"]
    
    assert enhanced_ml_score > base_ml_score
    print(f"Monotonicity verified: ML score rose from {base_ml_score}% to {enhanced_ml_score}%.")

def test_semantic_similarity_benchmark():
    text_tech1 = "Python backend developer specialized in microservices, FastAPI, and PostgreSQL database queries."
    text_tech2 = "Python engineer building REST APIs with FastAPI framework and relational Postgres databases."
    text_unrelated = "Floral arrangement specialist managing wedding bouquets, roses, and greenhouse plants."
    
    sim_related = SemanticMatcherService.compute_cosine_similarity(text_tech1, text_tech2)
    sim_unrelated = SemanticMatcherService.compute_cosine_similarity(text_tech1, text_unrelated)
    
    assert sim_related > sim_unrelated
    assert sim_related >= 0.08
    assert sim_unrelated <= 0.15
    print(f"Semantic similarity benchmark: Related={sim_related:.3f}, Unrelated={sim_unrelated:.3f}")
