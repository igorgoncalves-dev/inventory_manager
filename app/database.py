from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Connection URL
DATABASE_URL = "sqlite:///database.db"

# Database Connection and engine manager
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Session Manager
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# Declarative Base for Models
Base = declarative_base()

def session_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()




