from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. database import schemas
from .. crud import get_rooms
from .. dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.RoomCreate])
def read_rooms(db: Session = Depends(get_db)):
  return get_rooms(db)