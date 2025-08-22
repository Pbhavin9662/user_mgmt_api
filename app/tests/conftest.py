import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db

@pytest.fixture(scope="session")
def db_engine():
    # Use a temporary SQLite DB file for realistic behavior across connections
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    url = f"sqlite:///{db_path}"
    engine = create_engine(url, future=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    os.remove(db_path)

@pytest.fixture()
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False, future=True)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(db_session):
    # Override dependency
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
