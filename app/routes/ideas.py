from fastapi import APIRouter, Depends, HTTPException, status,Path
from app.models.idea import IdeaIn, IdeaOut,IdeaUpdate
from app.models.user import UserIn
from app.core.dependencies import get_current_user
from app.db.mongo import ideas_collection
from bson import ObjectId
from typing import List


router = APIRouter()

@router.post("/ideas", response_model=IdeaOut)
def create_idea(idea: IdeaIn, current_user: UserIn = Depends(get_current_user)):
    idea_dict = idea.dict()
    idea_dict["user_id"] = str(current_user["_id"])
    
    result = ideas_collection.insert_one(idea_dict)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create idea.")

    idea_dict["id"] = str(result.inserted_id)
    return IdeaOut(**idea_dict)

@router.get("/ideas" ,response_model=List[IdeaOut])
def get_ideas():
    ideas=[]
    for idea in ideas_collection.find():
        idea["id"] = str(idea.pop("_id"))
        ideas.append(IdeaOut(**idea))
    return ideas
@router.get("/ideas/me",response_model=List[IdeaOut])
def get_user_ideas(current_user: UserIn = Depends(get_current_user)):
    ideas=[]
    for idea in ideas_collection.find({"user_id": str(current_user["_id"])}):
        idea["id"] = str(idea.pop("_id"))
        ideas.append(IdeaOut(**idea))
    return ideas

@router.delete("/ideas/{id}")
def delete_idea(
    id: str = Path(..., description="The ID of the idea to delete"),
    current_user = Depends(get_current_user)
):
    idea = ideas_collection.find_one({"_id": ObjectId(id)})
    print(idea)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    if idea["user_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this idea")

    ideas_collection.delete_one({"_id": ObjectId(id)})
    return {"detail": "Idea deleted successfully"}

@router.patch("/ideas/{id}", response_model=IdeaOut)
def update_idea(id: str, idea: IdeaUpdate, current_user: dict = Depends(get_current_user)):
    idea_data = {k: v for k, v in idea.dict().items() if v is not None}
    if not idea_data:
        raise HTTPException(status_code=400, detail="No data to update.")

    result = ideas_collection.update_one(
        {"_id": ObjectId(id), "user_id": str(current_user["_id"])},
        {"$set": idea_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Idea not found.")

    updated = ideas_collection.find_one({"_id": ObjectId(id)})
    updated["id"] = str(updated.pop("_id"))
    return IdeaOut(**updated)