from . database import SessionLocal
from . models import Room
from . schemas import RoomBase
from .. crud import create_room

def init_database():
  db = SessionLocal()
  try:
    if db.query(Room).first() is None:
      initial_rooms = [
        RoomBase(name="Стандарт", description="Стандартная комната"),
        RoomBase(name="Премиум", description="Премиум комната"),
      ]
      for room_data in initial_rooms:
        create_room(db, room_data)
  finally:
    db.close()