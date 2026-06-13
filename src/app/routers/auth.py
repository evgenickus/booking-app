from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt
from passlib.context import CryptContext
from typing import Union
from datetime import datetime, timedelta, timezone
from .. utility import verify_password
from .. dependencies import get_db
from .. import crud
from .. database.schemas import UserBase, TokenData, Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
router = APIRouter()

SECRET_KEY = "2c4404d4c97419990d6c9f47719f50e487ef04e13f202f646460e2ccea2db1a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(login: str, password: str, db: Session = Depends(get_db)):
  user = crud.get_user_by_login(db, login)
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt
  
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    login: int = payload.get("sub")
    if login is None:
      raise credentials_exception
    token_data = TokenData(login=login)
  except jwt.exceptions.InvalidTokenError:
    raise credentials_exception
  user = crud.get_user_by_login(db, login=token_data.login)
  if user is None:
    raise credentials_exception
  return user

async def get_current_admin_user(
  current_user: UserBase = Depends(get_current_user)
):
  if not current_user.admin:
    raise HTTPException(status_code=403, detail="Доступ только для администратора")
  return current_user

async def verify_token(token: str = Depends(oauth2_scheme)):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    login: str = payload.get("sub")
    if login is None:
      raise HTTPException(status_code=403, detail="Token is invalid or expired")
    return payload
  except jwt.exceptions.InvalidTokenError:
    raise HTTPException(status_code=403, detail="Token is invalid or expired")
  

@router.get("/{token}")
async def verify_user_by_token(token: str):
  await verify_token(token=token)
  return {"message": "Token is valid"}

@router.post("/")
async def login_for_access_token(
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
  ) -> Token:
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Неверный логин или пароль",
      headers={"WWW-Authenticate": "Bearer"}
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={"sub": user.login}, expires_delta=access_token_expires
  )
  return Token(access_token=access_token, token_type="bearer")
