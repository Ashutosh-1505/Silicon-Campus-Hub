from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import LostFoundItem, User
from app.schema import lost_Found_Item, Lost_Found_Out
from app.core.db import get_db
from app.core.security import require_admin
from typing import List

router = APIRouter()


# ----------------------------
# POST /admin/lost_found  by Ashutosh Mohanty
# ----------------------------
@router.post("/admin/lost_found", status_code=201)
def create_lost_found(
    payload: lost_Found_Item,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    lost_found = LostFoundItem(
        title=payload.title,
        description=payload.description,
        is_found=payload.is_found,
        created_by=current_user.id
    )

    db.add(lost_found)
    db.commit()
    db.refresh(lost_found)

    return {
        "message": "Lost and Found created",
        "id": lost_found.id,
        "title": lost_found.title,
        "is_found": lost_found.is_found

    }

#---------------------------------------------------------------------------------
# GET /lostfound - Get full history of all lost & found items  by Sikhar Sambhab Mund
# --------------------------------------------------------------------------------
@router.get("/lostfound", response_model=List[Lost_Found_Out])
def list_lost_found_items(db: Session = Depends(get_db)):
    items = db.query(LostFoundItem).order_by(LostFoundItem.created_at.desc()).all()
    return items


#---------------------------------------------------------------------------------
# GET /lostfound/id - Get Lost and Found by id  by Ashutosh Das
# --------------------------------------------------------------------------------

@router.get("/lost-found/{id}", response_model=Lost_Found_Out)
def get_lost_found_item_id(id: int, db: Session = Depends(get_db)):
    item = db.query(LostFoundItem).filter(LostFoundItem.id == id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Lost/Found item not found")

    print(item)
    return item


#---------------------------------------------------------------------------------
# DELETE /lostfound/id - DELETE Lost and Found   by Asmit Raj
# --------------------------------------------------------------------------------

@router.delete("/{id}/delete", status_code=204)
def delete_lost_found_item(
    id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    lost_item = db.query(LostFoundItem).filter(LostFoundItem.id == id).first()

    if not lost_item:
        raise HTTPException(status_code=404, detail="Lost/Found item not found")

    db.delete(lost_item)
    db.commit()
    return {"message": "Item deleted successfully"}

