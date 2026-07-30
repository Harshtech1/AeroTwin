from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# Create engine (in production, use appropriate pooling/configurations)
engine = None
SessionLocal = None

if settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Database session dependency yield.
    """
    if SessionLocal is None:
        raise RuntimeError("Database URL is not configured.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
