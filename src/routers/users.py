from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Annotated
from .. database.schemas import UserBase, UserCreate
from .. crud import get_user_by_login, create_user, get_users
from .. dependencies import get_db

router = APIRouter()

@router.post("/", response_model=UserBase)
def add_user(
  user: Annotated[UserCreate, Query()],
  db: Session = Depends(get_db)
) -> UserBase:
  db_user = get_user_by_login(db, user.login)
  if db_user:
    raise HTTPException(status_code=409, detail=f"Пользователь с логином: {user.login} уже имеется")
  return create_user(db, user)

@router.get("/", response_model=List[UserBase])
def read_users(db: Session = Depends(get_db)):
  return get_users(db)
