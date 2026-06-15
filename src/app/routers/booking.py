from fastapi import APIRouter, HTTPException, Depends, Query, Body
from sqlalchemy.orm import Session
from typing import List, Annotated
from datetime import datetime, date
from .. database.schemas import UserBase, BookingBase, BookingGet, BookingCancel
from .. crud import get_room_by_name, create_booking, get_bookings_by_date, get_bookings, get_my_bookings, cancel_booking_admin, get_bookings_for_admin
from .. dependencies import get_db
from .. routers.auth import get_current_user, get_current_admin_user

router = APIRouter()

def get_free_slots(bookings, booking_date):
  slots = [i["slot"] for i in bookings]
  free_slots = [i for i in ["10-13", "14-17", "18-21"] if i not in slots]
  if booking_date == date.today():
    free_slots_correct = [i for i in free_slots if int(i[:2]) > datetime.now().hour]
    return free_slots_correct
  return free_slots
    
@router.post("/add",
  response_model=BookingBase,
  description=
    """
    Формат запроса:
    \n
    Укажите дату бронирования в формате YYYY-MM-DD
    Выберите комнату: Стандарт или Премиум
    Выберите слот: 10-13, 14-17, 18-21
    """
)
def add_booking(
  booking: BookingBase,         
  current_user: Annotated[UserBase, Depends(get_current_user)],
  db: Session = Depends(get_db)
) -> BookingBase:
  room_db = get_room_by_name(db, booking.room)
  bookings_db = get_bookings_by_date(db, booking, room_id=room_db.room_id)
  free_slots = get_free_slots(bookings_db, booking.booking_date)
  if booking.slot not in free_slots:
    raise HTTPException(status_code=409, detail=f"Этот слот занят")
  return create_booking(db, booking, user_id=current_user.user_id, room_id=room_db.room_id)

@router.get("/all", response_model=None)
def read_bookings(
  user = Depends(get_current_admin_user),
  db: Session = Depends(get_db)
):
  bookings_db = get_bookings(db)
  if bookings_db == []:
    return {"message": "Бронирования отсутствуют"}
  return bookings_db

@router.get("/free", response_model=None)
def check_free_slots(
  booking: Annotated[BookingGet, Query()],
  db: Session = Depends(get_db)
):
  room_db = get_room_by_name(db, booking.room)
  bookings_db = get_bookings_by_date(db, booking, room_id=room_db.room_id)
  free_slots = get_free_slots(bookings_db, booking.booking_date)
  if free_slots == []:
    return {"message": f"Свободных слотов на {booking.booking_date } нет"}
  return free_slots

@router.get("/my", response_model=None)
def read_my_bookings(
  current_user: Annotated[UserBase, Depends(get_current_user)],
  db: Session = Depends(get_db)
) -> List:
  bookings_db = get_my_bookings(db, user_id=current_user.user_id)
  if bookings_db == []:
    raise HTTPException(status_code=409, detail=f"У вас нет бронирований")
  return bookings_db

@router.put("/cancel",
  response_model=None,
  description=
    """
    Формат запроса:
    \n
    Укажите дату отмены бронирования в формате YYYY-MM-DD
    Выберите комнату: Стандарт или Премиум
    Выберите слот: 10-13, 14-17, 18-21
    """
)
def cancel_booking(
  booking: BookingCancel,
  current_user: Annotated[UserBase, Depends(get_current_user)],
  db: Session = Depends(get_db)
):
  room_db = get_room_by_name(db, booking.room)
  bookings_db = get_bookings_for_admin(db, booking, room_id=room_db.room_id)
  if bookings_db == []:
    raise HTTPException(status_code=409, detail=f"Бронирование с такими параметрами не найдено")
  elif bookings_db[0]["user_id"] != current_user.user_id and current_user.admin == False:
    raise HTTPException(status_code=409, detail=f"Отмена этого бронирования вам не доступно")
  
  return cancel_booking_admin(db, booking, user_id=bookings_db[0]["user_id"], room_id=room_db.room_id)
