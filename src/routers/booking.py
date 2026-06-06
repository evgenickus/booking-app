from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Annotated
from .. database import schemas
from .. import crud
from .. dependencies import get_db
from .. routers.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.BookingBase)
async def add_booking(
  booking: Annotated[schemas.BookingBase, Query()],
  current_user: Annotated[schemas.UserBase, Depends(get_current_user)],
  db: Session = Depends(get_db)
) -> schemas.BookingBase:
  room_db = crud.get_room_by_name(db, booking.room)
  if not room_db:
    raise HTTPException(status_code=409, detail=f"The room with name: '{booking.room}' is not exist")

#   db_booking = crud.get_booking_by_date(db, booking.booking_date)
#   if db_booking:
#     raise HTTPException(status_code=409, detail=f"There is not any free slots on: '{booking.booking_date}'")
  return crud.create_booking(db, booking, user_id=current_user.user_id, room_id=room_db.room_id)

@router.get("/", response_model=None)
# @router.get("/", response_model=List[schemas.BookingCreate])
def read_bookings(db: Session = Depends(get_db)):
  return crud.get_bookings(db)


