from fastapi import FastAPI
from app.core.db import Base, engine

from app.services.users import router as user_router
from app.services.announcement import router as announce_router
from app.services.lost_found import router as lost_found_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CampusHub")

@app.get("/")
def read_root():
    return {"message": "Welcome to CampusHub API 👋"}

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(announce_router, prefix="/announcements", tags=["Announcements"])
app.include_router(lost_found_router, prefix="/lost_found", tags=["Lost and Found"])
