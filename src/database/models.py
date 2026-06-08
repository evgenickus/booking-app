from datetime import datetime, date
from sqlalchemy import ForeignKey, String, Boolean, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base, engine

class User(Base):
  __tablename__ = "user"
  user_id: Mapped[int] = mapped_column(primary_key=True)
  login: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
  hashed_password: Mapped[str] = mapped_column(String, nullable=False)
  admin: Mapped[bool] = mapped_column(Boolean, default=False)

  def __repr__(self) -> str:
    return f"User(user_id={self.user_id!r}, login={self.login!r}, hashed_password={self.hashed_password!r}, admin={self.admin!r}"

class Room(Base):
  __tablename__= "room"
  room_id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
  description: Mapped[str] = mapped_column(String(250))

  def __repr__(self) -> str:
    return f"Room(room_id={self.room_id!r}, name={self.name!r}, description={self.description!r})"
  
class Booking(Base):
  __tablename__= "booking"
  booking_id: Mapped[int] = mapped_column(primary_key=True)
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), 
    server_default=func.now()
  )
  updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), 
    server_default=func.now(), 
    onupdate=func.now()
  )
  user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
  room_id: Mapped[int] = mapped_column(ForeignKey("room.room_id"))
  booking_date: Mapped[date] = mapped_column(Date)
  slot: Mapped[str] = mapped_column(String(10))
  status: Mapped[str] = mapped_column(String(10), default='active')

  def __repr__(self) -> str:
    return f"""
      Booking(
        booking_id={self.booking_id!r},
        created_at={self.created_at!r},
        updated_at={self.updated_at!r},
        user_id={self.user_id!r},
        room_id={self.room_id!r},
        booking_date={self.booking_date!r},
        slot={self.slot!r},
        status={self.status!r}
      )"""


Base.metadata.create_all(bind=engine)