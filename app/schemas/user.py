
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str