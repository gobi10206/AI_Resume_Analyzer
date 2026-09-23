import os
import sqlite3
import json
from typing import Any, Dict, List, Optional
from app.core.config import settings

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../resume_analyzer.db"))

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        full_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        version INTEGER DEFAULT 1,
        raw_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id TEXT PRIMARY KEY,
        resume_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        overall_score REAL NOT NULL,
        ats_score REAL NOT NULL,
        parsed_data TEXT NOT NULL,
        score_breakdown TEXT NOT NULL,
        strengths TEXT NOT NULL,
        weaknesses TEXT NOT NULL,
        ats_report TEXT NOT NULL,
        extracted_skills TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_roles (
        id TEXT PRIMARY KEY,
        title TEXT UNIQUE NOT NULL,
        department TEXT,
        experience_level TEXT,
        required_skills TEXT NOT NULL,
        optional_skills TEXT NOT NULL,
        required_education TEXT,
        minimum_experience_years REAL,
        sample_job_description TEXT,
        recommended_certifications TEXT,
        learning_path TEXT,
        sample_projects TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_matches (
        id TEXT PRIMARY KEY,
        analysis_id TEXT NOT NULL,
        role_id TEXT NOT NULL,
        match_percentage REAL NOT NULL,
        matching_skills TEXT NOT NULL,
        missing_skills TEXT NOT NULL,
        recommendation_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(analysis_id) REFERENCES analyses(id) ON DELETE CASCADE,
        FOREIGN KEY(role_id) REFERENCES job_roles(id) ON DELETE CASCADE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
        id TEXT PRIMARY KEY,
        analysis_id TEXT NOT NULL,
        target_role TEXT NOT NULL,
        roadmap_data TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    conn.close()
    seed_job_roles()

def seed_job_roles():
    data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/job_roles.json"))
    if not os.path.exists(data_file):
        return
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM job_roles")
    cnt = cursor.fetchone()["cnt"]
    
    if cnt == 0:
        import uuid
        with open(data_file, "r", encoding="utf-8") as f:
            roles = json.load(f)
        for r in roles:
            role_id = r.get("id") or str(uuid.uuid4())
            cursor.execute("""
            INSERT OR IGNORE INTO job_roles (
                id, title, department, experience_level, required_skills, optional_skills,
                required_education, minimum_experience_years, sample_job_description,
                recommended_certifications, learning_path, sample_projects
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                role_id,
                r.get("title"),
                r.get("department", "Engineering"),
                r.get("experience_level", "Mid-Level"),
                json.dumps(r.get("required_skills", [])),
                json.dumps(r.get("optional_skills", [])),
                r.get("required_education", "Bachelor's Degree in Computer Science or related"),
                float(r.get("minimum_experience_years", 2.0)),
                r.get("sample_job_description", ""),
                json.dumps(r.get("recommended_certifications", [])),
                json.dumps(r.get("learning_path", [])),
                json.dumps(r.get("sample_projects", []))
            ))
        conn.commit()
    conn.close()

init_db()
