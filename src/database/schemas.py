from pydantic import BaseModel, Field
from typing import Union, List, Literal
from datetime import datetime, date

class UserBase(BaseModel):
  user_id: int
  login: str

class UserCreate(BaseModel):
  login: str
  password: str
  admin: bool | None = None

class RoomBase(BaseModel):
  name: str
  description: str

class RoomCreate(RoomBase):
  room_id: int

class BookingBase(BaseModel):
  booking_date: date = Field(..., description="Укажите дату бронирования в формате YYYY-MM-DD")
  room: Literal["Standart", "Premium"] = Field(..., description="Выберите комнату для бронирования")
  slot: Literal["10-13", "14-17", "18-21"] = Field(..., description="Выберите время бронирования")

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