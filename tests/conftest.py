"""Shared test fixtures for LeadGenius."""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Force SQLite for tests so we don't need a running Postgres instance
os.environ["DATABASE_URL"] = "sqlite:///./test_leadgenius.db"

from backend.database import Base
from backend.main import app
from backend.database import get_db


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///./test_leadgenius.db",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    # Clean up test DB file
    if os.path.exists("./test_leadgenius.db"):
        os.remove("./test_leadgenius.db")


@pytest.fixture
def db_session(engine):
    """Provide a transactional DB session that rolls back after each test."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """FastAPI test client with overridden DB dependency."""
    from fastapi.testclient import TestClient

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
