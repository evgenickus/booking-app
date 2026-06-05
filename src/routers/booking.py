from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Annotated
from .. database import schemas
from .. import crud
from .. dependencies import get_db
from .. routers.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.BookingBase)
# def add_booking(booking: schemas.BookingBase, db: Session = Depends(get_db)):
async def add_booking(booking: Annotated[schemas.BookingBase, Query()], db: Session = Depends(get_db)):

#   db_booking = crud.get_booking_by_date(db, booking.booking_date)
#   if db_booking:
#     raise HTTPException(status_code=409, detail=f"There is not any free slots on: '{booking.booking_date}'")
  return crud.create_booking(db, booking, user_id=1)

@router.get("/", response_model=None)
# @router.get("/", response_model=List[schemas.BookingCreate])
def read_bookings(db: Session = Depends(get_db)):
  return crud.get_bookings(db)


