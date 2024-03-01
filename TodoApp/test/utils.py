from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from ..models import Todos, Users
from ..database import Base
from ..main import app
import pytest
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker( autocommit=False,
                                    autoflush=False,
                                    bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'testuser',
             'user_role': 'admin',
             'id': 1}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(title="test todo",
                 description="test description",
                 priority=1,
                 complete=False,
                 owner_id=1)
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos"))
        conn.commit()

@pytest.fixture
def test_user():
    user = Users(username="test",
                 email="test@email.com",
                 first_name = "test",
                 last_name = "user",	
                hashed_password=bcrypt_context.hash("password"),
                role="admin")
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()