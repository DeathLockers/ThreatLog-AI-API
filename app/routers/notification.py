from typing import Annotated
from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from ..services import (get_all_notifications,
                        update_read_notification,
                        update_all_read_notifications)
from ..schemas import (User as SchemaUser,
                       Notification as SchemaNotification)
from ..db import get_db
from ..core import (get_current_active_user,
                    limiter,
                    LIMIT_VALUE)
from ..validations import notification_id_exists

router = APIRouter(
    prefix="/notifications",
    tags=["notification"],
    responses={
       status.HTTP_401_UNAUTHORIZED: {
           "message": f"{'could_not_validate_credentials'}"
        },
        status.HTTP_404_NOT_FOUND: {"message": f"{'notification_not_found'}"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{'internal_server_error'}"
        },
    },
)


@router.get("/", response_model=list[SchemaNotification])
@limiter.limit(LIMIT_VALUE)
async def show_all_notifications(
  request: Request,
  current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
  db: Session = Depends(get_db)
):

  notifications = get_all_notifications(db, current_user.id)

  return notifications


@router.get("/{notification_id}/read", response_model=None, status_code=204)
@limiter.limit(LIMIT_VALUE)
async def read_notification(
  request: Request,
  current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
  notification_id: str,
  db: Session = Depends(get_db)
):

  notification_id_exists(current_user.id, notification_id)  # Validation

  update_read_notification(db, current_user.id, notification_id)

  return {}


@router.get("/read/all", response_model=None, status_code=204)
@limiter.limit(LIMIT_VALUE)
async def read_notification(
  request: Request,
  current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
  db: Session = Depends(get_db)
):

  update_all_read_notifications(db, current_user.id)

  return {}
