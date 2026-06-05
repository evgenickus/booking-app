from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from .. database import schemas
from .. import crud
from .. dependencies import get_db
from ..routers.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=schemas.UserBase)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_login(db, user.login)
  if db_user:
    raise HTTPException(status_code=409, detail=f"User with login: '{user.login}' already exists")
  return crud.create_user(db, user)

@router.get("/", response_model=List[schemas.UserBase])
def read_users(db: Session = Depends(get_db)):
  return crud.get_users(db)

@router.get("/hash", response_model=None)
def read_hash_password_by_login(login: str, db: Session = Depends(get_db)):
  return crud.get_user_hashpassword(db, login)

# @router.get("/profile/")
# async def get_profile(current_user: dict = Depends(get_current_user)):
#     # current_user уже содержит результат, не нужно await
#     return {"user": current_user}

@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[schemas.UserBase, Depends(get_current_active_user)],
) -> schemas.UserBase:
    return current_user

