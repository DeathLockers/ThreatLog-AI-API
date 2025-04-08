from datetime import datetime, timedelta
import jwt
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from ..core import (verify_password,
                    SECRET_KEY,
                    ALGORITHM,
                    ACCESS_TOKEN_EXPIRE_MINUTES,
                    credentials_exception,
                    getenv
                    )
from ..schemas import Token as SchemaToken


def login(db: Session, email: str, password: str):

  from ..services import get_user_by_email
  user = get_user_by_email(db, email)

  if not user:
    raise credentials_exception
  if not verify_password(password, user.hashed_password):
    raise credentials_exception

  return user


def login_access_token(user_email: str):

  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token, token_type = generate_access_token(
      data={"sub": user_email}, expires_delta=access_token_expires
  )

  return SchemaToken(access_token=access_token, token_type=token_type)


def generate_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  token_type = "bearer"

  if expires_delta:
    expire = datetime.now(ZoneInfo(getenv("TIMEZONE"))) + expires_delta

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(
      to_encode, SECRET_KEY, algorithm=ALGORITHM
  )

  return encoded_jwt, token_type


def extend_token_expiration(token: str) -> str:
  decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  token_type = "bearer"

  new_expiration = datetime.now(ZoneInfo(getenv("TIMEZONE"))) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  decoded_token["exp"] = new_expiration.timestamp()

  encoded_jwt = jwt.encode(decoded_token, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt, token_type
