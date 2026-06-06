from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func
from . database import schemas, models
from . import utility

# user

def create_user(db: Session, user: schemas.UserCreate):
  hashed_password = utility.hash_password(user.password)
  new_user = models.User(login=user.login, hashed_password=hashed_password, admin=user.admin)
  db.add(new_user)
  db.commit()
  return schemas.UserBase(user_id=new_user.user_id, login=new_user.login)

def get_users(db: Session):
  users = select(models.User)
  return db.scalars(users).all()

def get_user_id_by_user_login(db: Session, login: str):
  user_id = select(models.User).where(models.User.login == login)
  return db.scalar(user_id)

def get_user_hashpassword(db: Session, login: str):
  hashed_password = select(models.User.hashed_password).where(models.User.login == login)
  return db.scalar(hashed_password)

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