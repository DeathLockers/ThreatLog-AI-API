from typing import Annotated
from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from ..services import login, login_access_token
from ..db import get_db
from ..core import get_current_active_user, limiter, LIMIT_VALUE
from ..schemas import (Token as SchemaToken,
                       Login as SchemaLogin,
                       User as SchemaUser)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "message": f"{'could_not_validate_credentials'}"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{'internal_server_error'}"
        },
    },
)


@router.post("/login", response_model=SchemaToken)
@limiter.limit(LIMIT_VALUE)
async def login_for_access_token(
    request: Request, creedentials: SchemaLogin, db: Session = Depends(get_db)
):
  user = login(db, creedentials.email, creedentials.password)

  return login_access_token(user.email)


@router.get("/me", response_model=SchemaUser)
@limiter.limit(LIMIT_VALUE)
async def read_auth_me(
    request: Request,
    current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
):

  return current_user
