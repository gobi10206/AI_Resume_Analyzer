import os
import uuid
import json
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db_connection
from app.schemas.resume import ResumeUploadResponse, ResumeListItem
from app.services.parser import ResumeParserService
from app.services.nlp_extractor import NLPExtractorService
from app.services.scoring_engine import ScoringEngineService
from app.services.ats_analyzer import AtsAnalyzerService

router = APIRouter(prefix="/resumes", tags=["Resumes"])

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    filename = file.filename or "resume.pdf"
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format '{ext}'. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
        
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB."
        )
        
    resume_id = str(uuid.uuid4())
    saved_filename = f"{resume_id}{ext}"
    saved_path = os.path.join(settings.UPLOAD_DIR, saved_filename)
    
    with open(saved_path, "wb") as f:
        f.write(content)
        
    # 1. Parse document text and structure
    try:
        parsed_doc = ResumeParserService.parse_file(content, filename)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse document: {str(e)}"
        )
        
    raw_text = parsed_doc["raw_text"]
    metadata = parsed_doc["metadata"]
    sections = parsed_doc["sections"]
    
    # 2. Extract entities via NLP
    entities = NLPExtractorService.extract_entities(raw_text, sections, metadata)
    
    # 3. Evaluate 0-100 score & ATS score
    eval_res = ScoringEngineService.evaluate(entities, raw_text, metadata)
    ats_report = AtsAnalyzerService.analyze(entities, raw_text, metadata, sections)
    
    # 4. Save resume & initial analysis into DB
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check current version count for user
    cursor.execute("SELECT COUNT(*) as cnt FROM resumes WHERE user_id = ?", (current_user["id"],))
    version_count = cursor.fetchone()["cnt"] + 1
    
    cursor.execute("""
    INSERT INTO resumes (id, user_id, file_name, file_path, file_type, file_size, version, raw_text)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (resume_id, current_user["id"], filename, saved_path, ext, file_size, version_count, raw_text))
    
    analysis_id = str(uuid.uuid4())
    cursor.execute("""
    INSERT INTO analyses (
        id, resume_id, user_id, overall_score, ats_score, parsed_data,
        score_breakdown, strengths, weaknesses, ats_report, extracted_skills
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        analysis_id,
        resume_id,
        current_user["id"],
        eval_res["overall_score"],
        ats_report.ats_score,
        json.dumps(entities.dict()),
        json.dumps(eval_res["score_breakdown"].dict()),
        json.dumps([s.dict() for s in eval_res["strengths"]]),
        json.dumps([w.dict() for w in eval_res["weaknesses"]]),
        json.dumps(ats_report.dict()),
        json.dumps(entities.skills)
    ))
    
    conn.commit()
    conn.close()
    
    return ResumeUploadResponse(
        id=resume_id,
        file_name=filename,
        file_type=ext,
        file_size=file_size,
        version=version_count,
        created_at=str(metadata.get("created_at", "Just now")),
        raw_text_preview=raw_text[:350] + ("..." if len(raw_text) > 350 else "")
    )

@router.get("", response_model=List[ResumeListItem])
def list_resumes(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT r.*, (SELECT COUNT(*) FROM analyses a WHERE a.resume_id = r.id) as analysis_count
    FROM resumes r
    WHERE r.user_id = ?
    ORDER BY r.created_at DESC
    """, (current_user["id"],))
    rows = cursor.fetchall()
    conn.close()
    
    items = []
    for row in rows:
        items.append(ResumeListItem(
            id=row["id"],
            file_name=row["file_name"],
            file_type=row["file_type"],
            file_size=row["file_size"],
            version=row["version"],
            created_at=str(row["created_at"]),
            has_analysis=row["analysis_count"] > 0
        ))
    return items

@router.get("/{resume_id}")
def get_resume_detail(resume_id: str, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes WHERE id = ? AND user_id = ?", (resume_id, current_user["id"]))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Resume not found")
    return dict(row)

@router.delete("/{resume_id}")
def delete_resume(resume_id: str, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM resumes WHERE id = ? AND user_id = ?", (resume_id, current_user["id"]))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Resume not found")
        
    file_path = row["file_path"]
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass
            
    cursor.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
    cursor.execute("DELETE FROM analyses WHERE resume_id = ?", (resume_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Resume and associated analyses deleted permanently."}
