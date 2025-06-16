from pydantic import BaseModel,EmailStr
from datetime import datetime

class CreateUser(BaseModel):
    email : EmailStr
    password:str

class UserOut(BaseModel):
    id:str
    email :EmailStr
    created_at:datetime

class UserIn(BaseModel):
    email :EmailStr
    hashed_password:str
    created_at:datetime