from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.ideas import router as idea_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(idea_router)
