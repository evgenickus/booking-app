from sqlalchemy.orm import Session
from sqlalchemy import select, update
from . database import schemas, models
from . import utility

# user

def create_user(db: Session, user: schemas.UserCreate):
  hashed_password = utility.hash_password(user.password)
  new_user = models.User(login=user.login, hashed_password=hashed_password, admin=user.admin)
  db.add(new_user)
  db.commit()
  return schemas.UserBase(user_id=new_user.user_id, login=new_user.login, admin=new_user.admin)

def get_users(db: Session):
  users = select(models.User)
  return db.scalars(users).all()

def get_user_by_login(db: Session, login: str):
  user = select(models.User).where(models.User.login == login)
  return db.scalar(user)

#rooms
def create_room(db: Session, room: schemas.RoomCreate):
  new_room = models.Room(name=room.name, description=room.description)
  db.add(new_room)
  db.commit()
  return schemas.RoomBase(name=new_room.name, description=new_room.description)

def get_rooms(db: Session):
  rooms = select(models.Room)
  return db.scalars(rooms).all()

def get_room_by_name(db: Session, name: str):
  room = select(models.Room).where(models.Room.name == name)
  return db.scalar(room)

# booking

def create_booking(db: Session, booking: schemas.BookingCreate, user_id, room_id):
  new_booking = models.Booking(booking_date=booking.booking_date, slot=booking.slot, user_id=user_id, room_id=room_id)
  db.add(new_booking)
  db.commit()
  return schemas.BookingBase(booking_date=new_booking.booking_date, room=booking.room, slot=new_booking.slot)

def get_bookings(db: Session):
  bookings = select(models.Booking)
  return db.scalars(bookings).all()

def get_bookings_by_date(db: Session, booking: schemas.BookingGet, room_id):
  bookings = select(
    models.Booking.slot,
    models.Booking.booking_date,
    models.Booking.status,
    models.Room.name
  ).join(models.Room
  ).where(models.Booking.booking_date == booking.booking_date
  ).where(models.Booking.room_id == room_id
  ).where(models.Booking.status == "active")
  result = db.execute(bookings).all()
  return [row._asdict() for row in result]

def get_bookings_by_params(db: Session, booking: schemas.BookingCancel, room_id, user_id):
  bookings = select(
    models.Booking.slot,
    models.Booking.booking_date,
    models.Booking.status,
    models.Room.name
  ).join(models.Room
  ).where(models.Booking.booking_date == booking.booking_date
  ).where(models.Booking.slot == booking.slot
  ).where(models.Booking.room_id == room_id
  ).where(models.Booking.user_id == user_id
  ).where(models.Booking.status == "active")
  result = db.execute(bookings).all()
  return [row._asdict() for row in result]

def get_my_bookings(db: Session, user_id):
  bookings = select(
    models.Booking.slot,
    models.Booking.booking_date,
    models.Room.name).join(models.Room).where(
    models.Booking.user_id == user_id
  ).where(models.Booking.status == "active")
  result = db.execute(bookings).all()
  return [row._asdict() for row in result]

def cancel_booking(db: Session, booking: schemas.BookingCancel, user_id, room_id):
  update_booking = update(models.Booking
  ).where(models.Booking.booking_date == booking.booking_date
  ).where(models.Booking.slot == booking.slot
  ).where(models.Booking.user_id == user_id
  ).where(models.Booking.room_id == room_id
  ).where(models.Booking.status == "active"
  ).values(status="canceled")
  db.execute(update_booking)
  db.commit()
  return {"msg": f"Это бронирование {booking.booking_date, booking.slot, booking.room} отменено"}
