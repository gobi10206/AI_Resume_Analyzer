"""
SQLAlchemy database models for PostgreSQL deployment.
"""
try:
    from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey, Boolean
    from sqlalchemy.orm import relationship
    from sqlalchemy.sql import func
    from app.models import Base

    class User(Base):
        __tablename__ = "users"
        id = Column(String, primary_key=True, index=True)
        email = Column(String, unique=True, index=True, nullable=False)
        hashed_password = Column(String, nullable=False)
        full_name = Column(String, nullable=True)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        updated_at = Column(DateTime(timezone=True), onupdate=func.now())
        
        resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
        analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")

    class Resume(Base):
        __tablename__ = "resumes"
        id = Column(String, primary_key=True, index=True)
        user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
        file_name = Column(String, nullable=False)
        file_path = Column(String, nullable=False)
        file_type = Column(String, nullable=False)
        file_size = Column(Integer, nullable=False)
        version = Column(Integer, default=1)
        raw_text = Column(Text, nullable=True)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        
        user = relationship("User", back_populates="resumes")
        analyses = relationship("Analysis", back_populates="resume", cascade="all, delete-orphan")

    class Analysis(Base):
        __tablename__ = "analyses"
        id = Column(String, primary_key=True, index=True)
        resume_id = Column(String, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
        user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
        overall_score = Column(Float, nullable=False)
        ats_score = Column(Float, nullable=False)
        parsed_data = Column(Text, nullable=False)        # JSON string
        score_breakdown = Column(Text, nullable=False)    # JSON string
        strengths = Column(Text, nullable=False)          # JSON string
        weaknesses = Column(Text, nullable=False)         # JSON string
        ats_report = Column(Text, nullable=False)         # JSON string
        extracted_skills = Column(Text, nullable=False)   # JSON string
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        
        resume = relationship("Resume", back_populates="analyses")
        user = relationship("User", back_populates="analyses")

    class JobRole(Base):
        __tablename__ = "job_roles"
        id = Column(String, primary_key=True, index=True)
        title = Column(String, unique=True, index=True, nullable=False)
        department = Column(String, nullable=True)
        experience_level = Column(String, nullable=True)
        required_skills = Column(Text, nullable=False)     # JSON string
        optional_skills = Column(Text, nullable=False)     # JSON string
        required_education = Column(String, nullable=True)
        minimum_experience_years = Column(Float, default=2.0)
        sample_job_description = Column(Text, nullable=True)
        recommended_certifications = Column(Text, nullable=True) # JSON
        learning_path = Column(Text, nullable=True)        # JSON
        sample_projects = Column(Text, nullable=True)      # JSON
        created_at = Column(DateTime(timezone=True), server_default=func.now())

except ImportError:
    pass
