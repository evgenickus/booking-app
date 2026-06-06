from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Annotated
from .. database import schemas
from .. import crud
from .. dependencies import get_db

router = APIRouter()

# @router.post("/", response_model=schemas.RoomBase)
# def add_room(room: schemas.RoomBase, db: Session = Depends(get_db)):
#   db_room = crud.get_room_by_name(db, room.name)
#   if db_room:
#     raise HTTPException(status_code=409, detail=f"Room with name: '{room.name}' already exists")
#   return crud.create_room(db, room)

# @router.get("/", response_model=List[schemas.RoomCreate])
# def read_rooms(db: Session = Depends(get_db)):
#   return crud.get_rooms(db)

# @router.get("/room", response_model=None)
# def read_room_id(name: str, db: Session = Depends(get_db)):
#   return crud.get_room_by_name(db, name)

# @router.get("/", response_model=None)
# def get_free_slots(room: schemas.RoomBase, db: Session = Depends(get_db)):
#   return room
