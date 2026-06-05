from pydantic import BaseModel, Field
from typing import Union, List, Literal
from datetime import datetime, date


class UserBase(BaseModel):
  user_id: int
  login: str
  disabled: bool | None = None

class UserCreate(BaseModel):
  login: str
  password: str
  admin: bool

class UserInDB(UserBase):
  hashed_password: str
  admin: bool

class RoomBase(BaseModel):
  name: str
  description: str

class RoomCreate(RoomBase):
  room_id: int

class BookingBase(BaseModel):
  # booking_date: datetime.date
  # slot: str
  booking_date: date = Field(..., description="Укажите дату бронирования в формате YYYY-MM-DD")
  slot: Literal["10-13", "13-17", "17-20"] = Field(..., description="Выберите время бронирования")

class BookingCreate(BookingBase):
  booking_id: int
  created_at: datetime
  updated_at: datetime
  user_id: int
  room_id: int
  status: List[str] = Field(default_factory=lambda: ["active", "canceled"])

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  login: Union[str, None] = None