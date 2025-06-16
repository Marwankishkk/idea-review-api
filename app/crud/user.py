# app/crud/user.py

from pymongo.collection import Collection
from app.schemas.user import UserCreate, UserInDB
from app.core.security import hash_password

def get_user_by_email(users_collection: Collection, email: str) -> dict | None:
    return users_collection.find_one({"email": email})

def create_user(users_collection: Collection, user: UserCreate) -> UserInDB:
    hashed_pw = hash_password(user.password)
    user_data = {"email": user.email, "hashed_password": hashed_pw}
    users_collection.insert_one(user_data)
    return UserInDB(**user_data)
