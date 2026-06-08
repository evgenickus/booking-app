from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Annotated
from .. database.schemas import UserBase, BookingBase, BookingGet, BookingCancel
from .. crud import get_room_by_name, create_booking, get_bookings_by_date, get_bookings_by_params, get_bookings, get_my_bookings, cancel_booking
from .. dependencies import get_db
from .. routers.auth import get_current_user

router = APIRouter()

def get_free_slots(bookings):
  slots = [i["slot"] for i in bookings]
  free_slots = [i for i in ["10-13", "14-17", "18-21"] if i not in slots]
  return free_slots
    
@router.post("/", response_model=BookingBase)
def add_booking(
  booking: Annotated[BookingBase, Query()],
  current_user: Annotated[UserBase, Depends(get_current_user)],
  db: Session = Depends(get_db)
) -> BookingBase:
  room_db = get_room_by_name(db, booking.room)
  bookings_db = get_bookings_by_date(db, booking, room_id=room_db.room_id)
  free_slots = get_free_slots(bookings_db)

  if booking.slot not in free_slots:
    raise HTTPException(status_code=409, detail=f"Этот слот занят")
  return create_booking(db, booking, user_id=current_user.user_id, room_id=room_db.room_id)

@router.get("/all", response_model=None)
def read_bookings(db: Session = Depends(get_db)):
  bookings_db = get_bookings(db)
  if bookings_db == []:
    raise HTTPException(status_code=409, detail=f"Резервирований нет")
  return bookings_db

@router.get("/", response_model=None)
def check_free_slots(
  booking: Annotated[BookingGet, Query()],
  db: Session = Depends(get_db)
):
  room_db = get_room_by_name(db, booking.room)
  bookings_db = get_bookings_by_date(db, booking, room_id=room_db.room_id)
  free_slots = get_free_slots(bookings_db)
  if free_slots == []:
    raise HTTPException(status_code=409, detail=f"На выбранную дату слотов нет")
  return free_slots

@router.get("/my_bookings", response_model=None)
def read_my_bookings(
  current_user: Annotated[UserBase, Depends(get_current_user)],
  db: Session = Depends(get_db)
) -> List:
  bookings_db = get_my_bookings(db, user_id=current_user.user_id)
  if bookings_db == []:
    raise HTTPException(status_code=409, detail=f"У вас нет резервирований")
  return bookings_db

@router.put("/", response_model=None)
def cancel_my_booking(
  booking: Annotated[BookingCancel, Query()],
  current_user: Annotated[UserBase, Depends(get_current_user)],
  db: Session = Depends(get_db)
):
  room_db = get_room_by_name(db, booking.room)
  bookings_db = get_bookings_by_params(db, booking, room_id=room_db.room_id, user_id = current_user.user_id)
  if bookings_db == []:
    raise HTTPException(status_code=409, detail=f"Резервирование с такими параметрами не найдено")
  return cancel_booking(db, booking, user_id=current_user.user_id, room_id=room_db.room_id)

@router.put("/admin", response_model=None)
def cancel_booking_for_admin(
  booking: Annotated[BookingCancel, Query()],
  current_user: Annotated[UserBase, Depends(get_current_user)],
  db: Session = Depends(get_db)
):
  room_db = get_room_by_name(db, booking.room)
  bookings_db = get_bookings_by_params(db, booking, room_id=room_db.room_id)
  if bookings_db == []:
    raise HTTPException(status_code=409, detail=f"Резервирование с такими параметрами не найдено")
  return cancel_booking(db, booking, user_id=current_user.user_id, room_id=room_db.room_id)
