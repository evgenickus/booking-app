from . database import SessionLocal
from . models import Room
from . schemas import RoomBase
from .. crud import create_room

def init_database() -> None:
  """
  В блоке try

  Проверяется созданы ли комнаты в базе, если нет то вызывается
  метод create_room и данные по комнатам добавляются базу
  
  В блоке finally

  происходит закрытие бызы

  """
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