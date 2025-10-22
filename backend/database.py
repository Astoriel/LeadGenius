import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use internal docker dns or fallback to localhost
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://leaduser:leadpassword@localhost:5432/leadgenius")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
