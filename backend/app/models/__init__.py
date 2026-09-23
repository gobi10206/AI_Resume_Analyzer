# SQLAlchemy Declarative Models for PostgreSQL / Alembic
try:
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
except ImportError:
    Base = object
