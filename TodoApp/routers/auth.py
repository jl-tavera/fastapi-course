from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, max_length=100)
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    role: str = Field(min_length=3, max_length=100)
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(db: db_dependency, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return {"detail": "Incorrect username or password"}
    
    return 'Success!'
    

