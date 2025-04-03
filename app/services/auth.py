from datetime import datetime, timedelta, timezone
import jwt
from sqlalchemy.orm import Session
from ..core import (verify_password,
                    SECRET_KEY,
                    ALGORITHM,
                    ACCESS_TOKEN_EXPIRE_MINUTES,
                    email_not_exists_exception,
                    login_incorrect_exception
                    )
from ..schemas import Token as SchemaToken


def login(db: Session, email: str, password: str):

  from ..services import get_user_by_email
  user = get_user_by_email(db, email)

  if not user:
    raise email_not_exists_exception
  if not verify_password(password, user.hashed_password):
    raise login_incorrect_exception

  return user


def login_access_token(user_email: str):

  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = generate_access_token(
      data={"sub": user_email}, expires_delta=access_token_expires
  )

  return SchemaToken(access_token=access_token, token_type="bearer")


def generate_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()

  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(
      to_encode, SECRET_KEY, algorithm=ALGORITHM
  )

  return encoded_jwt
