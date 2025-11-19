from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Announcement, User
from app.schema import announcementCreate, announcementOut
from app.core.db import get_db
from app.core.security import require_admin
from typing import List

router = APIRouter()

# ----------------------------
# GET /announcements
# ----------------------------
@router.get("/announcements", response_model=List[announcementOut])
def list_announcements(db: Session = Depends(get_db)):
    announcements = db.query(Announcement).order_by(Announcement.created_at.desc()).all()

    print(announcements)
    return announcements


# ----------------------------
# POST /admin/announcements
# ----------------------------
@router.post("/admin/announcements", status_code=201)
def create_announcement(
    payload: announcementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    announcement = Announcement(
        title=payload.title,
        content=payload.content,
        created_by=current_user.id
    )
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return {"message": "Announcement created", "id": announcement.id}


# ----------------------------
# DELETE /admin/announcements/{id}/delete
# ----------------------------
@router.delete("/admin/announcements/{id}/delete")
def delete_announcement(
    id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    announcement = db.query(Announcement).filter(Announcement.id == id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    db.delete(announcement)
    db.commit()
    return {"message": "Announcement deleted"}


# ----------------------------
# GET BY ID /admin/announcements/{id}/get by sandeep kumar sahoo
# ----------------------------


@router.get("/admin/announcements/{id}", response_model=announcementOut)
def get_announcement_by_id(id: int, db: Session = Depends(get_db)):
    announcement = db.query(Announcement).filter(Announcement.id == id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return announcement
#---------------------------
