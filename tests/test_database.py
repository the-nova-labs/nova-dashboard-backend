from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base

# Use SQLite in-memory database for testing
TEST_DATABASE_URL = "sqlite:///test-nova-leaderboard-v2.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Dependency override to use test DB."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables in the test database
Base.metadata.create_all(bind=engine)
