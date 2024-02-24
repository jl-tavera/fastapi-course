from fastapi import APIRouter
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, max_length=100)
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    role: str = Field(min_length=3, max_length=100)
    

@router.post("/auth/")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    return create_user_model
    

