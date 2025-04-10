from typing import Annotated
from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from ..services import (upsert_verified_log)
from ..schemas import (User as SchemaUser,
                       UpsertVerifiedLog as SchemaUpsertVerifiedLog)
from ..db import get_db
from ..core import (get_current_active_user,
                    limiter,
                    LIMIT_VALUE)

router = APIRouter(
    prefix="/verified_logs",
    tags=["verified_log"],
    responses={
       status.HTTP_401_UNAUTHORIZED: {
           "message": f"{'could_not_validate_credentials'}"
        },
        status.HTTP_404_NOT_FOUND: {"message": f"{'log_not_found'}"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{'internal_server_error'}"
        },
    },
)


@router.post("/", response_model=None, status_code=204)
@limiter.limit(LIMIT_VALUE)
async def ins_upt_del_verified_log(
  request: Request,
  current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
  verified_log: SchemaUpsertVerifiedLog,
  db: Session = Depends(get_db)
):

  upsert_verified_log(db, verified_log)

  return {}
