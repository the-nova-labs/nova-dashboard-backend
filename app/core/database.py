from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.constants import DATABASE_URL
from app.models.models import Base


engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
