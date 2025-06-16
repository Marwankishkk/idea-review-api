from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class IdeaIn(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = []
    rating: Optional[float] = None

class IdeaOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    rating: Optional[float] = None
    user_id: str

    class Config:
        orm_mode = True

class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    rating: Optional[float] = None