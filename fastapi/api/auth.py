from datetime import timedelta, datetime, timezone
from typing import Annonated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAUTH2PasswordRequestForm
from jose import jwt
from dotenv import load_dotenv
import os
import api.models import User
from api.deps import db_dependency, bcrypt_context

load_dotenv()

router = APIRouter(
  prefix='/auth',
  tags=['auth']
)

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

class UserCreateRequest(BaseModel):
  username: str
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

def authenticate_user(username: str, password:str, db):
  user = db.query(User).filter(User.username == username).first()
  if not user:
    return False
  if not bcrypt_context.verify(password, user.hashed_password):
    return False
  return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
  encode = {'sub': username, 'id': user_id}
  expires = datetime.now(timezone.utc) + expires_delta
  encode.update({'exp': expires})
  return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserCreateRequest):
  create_user_model = User(
    username=create_user_request.username,
    hashed_password=bcrypt_context.hash(create_user_request.password)
  )
  db.add(create_user_model)
  db.commit()

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
  


