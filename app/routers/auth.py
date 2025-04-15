from typing import Annotated
from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from ..services import (login,
                        login_access_token,
                        extend_token_expiration)
from ..db import get_db
from ..core import (get_current_active_user,
                    get_current_token,
                    limiter,
                    LIMIT_VALUE)
from ..schemas import (UserAuth as SchemaUserAuth,
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


@router.post("/login", response_model=SchemaUserAuth)
@limiter.limit(LIMIT_VALUE)
async def login_for_access_token(
    request: Request, creedentials: SchemaLogin, db: Session = Depends(get_db)
):
  user = login(db, creedentials.email, creedentials.password)

  token = login_access_token(user.email)

  return {
    'id': user.id,
    'name': user.name,
    'email': user.email,
    'token': f"{token.token_type} {token.access_token}"
  }


@router.get("/me", response_model=SchemaUserAuth)
@limiter.limit(LIMIT_VALUE)
async def read_auth_me(
    request: Request,
    current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
    token: Annotated[str, Depends(get_current_token)],
):

  token, token_type = extend_token_expiration(token)

  return {
    'id': current_user.id,
    'name': current_user.name,
    'email': current_user.email,
    'token': f"{token_type} {token}"
  }
