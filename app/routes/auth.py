# app/routes/auth.py
from fastapi import Depends
from app.core.dependencies import get_current_user
from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate,LoginRequest,RefreshTokenRequest
from app.db.mongo import users_collection
from app.crud.user import get_user_by_email, create_user
from app.core.security import verify_password,create_access_token,create_refresh_token,SECRET_KEY,ALGORITHM
from jose import JWTError,jwt
from bson import ObjectId


router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    existing_user = get_user_by_email(users_collection, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    created_user = create_user(users_collection, user)
    return {"message": "User registered successfully", "email": created_user.email}

@router.post("/login")
def login(request:LoginRequest):
    user=users_collection.find_one({"email": request.email})
    if not user or not verify_password(request.password,user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token=create_access_token(str(user["_id"]))

    refresh_token=create_refresh_token({"sub": str(user["_id"])})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }                            


@router.get("/me")
def get_my_profile(current_user = Depends(get_current_user)):
    return {"email": current_user["email"], "id": str(current_user["_id"])}

@router.post("/refresh")
def refresh_token(data: RefreshTokenRequest):
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": new_access_token}