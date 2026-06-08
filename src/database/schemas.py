from pydantic import BaseModel, Field, field_validator
from typing import Union, List, Literal
from datetime import datetime, date

class UserBase(BaseModel):
  login: str
  admin: bool

class UserCreate(BaseModel):
  login: str
  password: str
  admin: Literal[False, True] = Field(..., description="Укажите является ли пользователь администратором")
  
  @field_validator('admin', mode='before')
  def coerce_admin(cls, v):
    if isinstance(v, str):
      if v.lower() == 'true':
        return True
      elif v.lower() == 'false':
        return False
    return v

class RoomBase(BaseModel):
  name: str
  description: str

class RoomCreate(RoomBase):
  room_id: int

class BookingBase(BaseModel):
  booking_date: date = Field(..., description="Укажите дату бронирования в формате YYYY-MM-DD")
  room: Literal["Стандарт", "Премиум"] = Field(..., description="Выберите комнату для бронирования")
  slot: Literal["10-13", "14-17", "18-21"] = Field(..., description="Выберите время бронирования")
  
  @field_validator("booking_date")
  def validate_date_not_in_future(cls, v: date) -> date:
    if v < date.today():
      raise ValueError("Дата не может быть позже сегодняшнего дня")
    return v

class BookingCreate(BookingBase):
  booking_id: int
  created_at: datetime
  updated_at: datetime
  user_id: int
  room_id: int
  status: List[str] = Field(default_factory=lambda: ["active", "canceled"])

class BookingGet(BaseModel):
  booking_date: date = Field(..., description="Укажите дату в формате YYYY-MM-DD")
  room: Literal["Стандарт", "Премиум"] = Field(..., description="Выберите комнату")

class BookingCancel(BaseModel):
  booking_date: date = Field(..., description="Укажите дату отмены бронирования в формате YYYY-MM-DD")
  room: Literal["Стандарт", "Премиум"] = Field(..., description="Выберите комнату для отмены бронирования")
  slot: Literal["10-13", "14-17", "18-21"] = Field(..., description="Выберите слот")

  @field_validator("booking_date")
  def validate_date_not_in_future(cls, v: date) -> date:
    if v < date.today():
      raise ValueError("Дата не может быть позже сегодняшнего дня")
    return v
  
class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  login: Union[str, None] = None