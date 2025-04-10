from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from ...core import oauth2_scheme
from .config import ALGORITHM, SECRET_KEY
from ..http_exceptions import credentials_exception, forbidden_exception
from ...schemas import (TokenData as SchemaTokenData,
                        User as SchemaUser)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
  return verify_access_token(token)

async def get_token(token: Annotated[str, Depends(oauth2_scheme)]):
  return token


async def get_current_active_user(
    current_user: Annotated[SchemaUser, Depends(get_current_user)],
):
  return current_user


def verify_access_token_websocket(token: str):
  return verify_access_token(token)


def get_current_user_wewbsocket(token: str):
  if token:
    token = token.replace("bearer ", "")
  else:
    token = ""

  return verify_access_token_websocket(token)


def verify_access_token(token):
  try:
    payload = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM]
    )

    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception

    token_data = SchemaTokenData(username=username)
  except InvalidTokenError:
    raise credentials_exception

  from ...services import get_user_by_email
  from ...db import engine

  user = get_user_by_email(Session(engine), token_data.username)
  if user is None:
    raise forbidden_exception

  return user

async def get_current_token(
    token: Annotated[SchemaUser, Depends(get_token)],
):
  return token