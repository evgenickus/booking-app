from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Union, List, Literal
from datetime import datetime, date, timedelta

class UserBase(BaseModel):
  login: str
  admin: bool

class UserCreate(BaseModel):
  login: str
  password: str
  admin: Literal[False, True] = Field(..., description="Укажите является ли пользователь администратором")
  
  @field_validator('admin', mode='before')
  @classmethod
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
  room: Literal["Стандарт", "Премиум"] = Field(..., description="Выберите комнату")
  slot: Literal["10-13", "14-17", "18-21"] = Field(..., description="Выберите слот")
  
  @field_validator("booking_date")
  @classmethod
  def validate_date_not_in_past(cls, v: date) -> date:
    if v < date.today():
      raise ValueError("Дата не может быть позже сегодняшнего дня")
    return v

  @field_validator("slot")
  @classmethod
  def validate_slot_not_in_past(cls, v: str, info: ValidationInfo) -> str:
    booking_date = info.data.get("booking_date")
    if booking_date is None:
      return v
    elif booking_date > date.today():
      return v
    if int(v[:2]) <= datetime.now().hour:
      raise ValueError("Бронирование невозможно после начала слота")
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
  
  @field_validator("booking_date")
  @classmethod
  def validate_date_not_in_future(cls, v: date) -> date:
    if v < date.today():
      raise ValueError("Дата не может быть позже сегодняшнего дня")
    return v
  
class BookingCancel(BaseModel):
  booking_date: date = Field(..., description="Укажите дату отмены бронирования в формате YYYY-MM-DD")
  room: Literal["Стандарт", "Премиум"] = Field(..., description="Выберите комнату")
  slot: Literal["10-13", "14-17", "18-21"] = Field(..., description="Выберите слот")

  @field_validator("booking_date")
  @classmethod
  def validate_date_not_in_past(cls, v: date) -> date:
    if v < date.today():
      raise ValueError("Дата не может быть позже сегодняшнего дня")
    return v

  @field_validator("slot")
  @classmethod
  def validate_slot_not_in_past(cls, v: str, info: ValidationInfo) -> str:
    booking_date = info.data.get("booking_date")
    if booking_date is None:
      return v
    elif booking_date > date.today():
      return v
    if int(v[:2]) <= datetime.now().hour:
      raise ValueError("Отмена бронирования невозможно после начала слота")
    return v
  
class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  login: Union[str, None] = None