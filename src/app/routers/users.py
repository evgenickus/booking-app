from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from .. database.schemas import UserBase, UserCreate
from .. crud import get_user_by_login, create_user, get_users
from .. dependencies import get_db

router = APIRouter()

@router.post("/add",
  response_model=UserBase,
  description=
    """
    Формат запроса:
    \n
    Для регистрации нового пользователя укажите его логин и пароль
    Значение для поля admin укажите: false или true
    """
)
def add_user(
  # user: Annotated[UserCreate, Query()],
  user: UserCreate,
  db: Session = Depends(get_db)
) -> UserBase:
  db_user = get_user_by_login(db, user.login)
  # print(db_user)
  if db_user:
    raise HTTPException(status_code=409, detail=f"Пользователь с логином: {user.login} уже имеется")
  return create_user(db, user)

@router.get("/all", response_model=List[UserBase])
def read_users(db: Session = Depends(get_db)):
  return get_users(db)
