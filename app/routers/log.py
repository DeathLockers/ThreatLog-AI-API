from typing import Annotated
from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from ..services import (get_logs,
                        count_logs_in_time_periods,
                        total_type_logs_in_period,
                        count_type_logs_in_period)
from ..schemas import (User as SchemaUser,
                       Log as SchemaLog,
                       LogFilter as SchemaLogFilter,
                       LogChartLinePeriod as SchemaLogChartLinePeriod,
                       LogChartTypesCountPeriod as SchemaLogChartTypesCountPeriod,
                       LogTypesTotal as SchemaLogTypesTotal)
from ..db import get_db
from ..core import (get_current_active_user,
                    get_last_half_hour,
                    limiter,
                    LIMIT_VALUE)

router = APIRouter(
    prefix="/logs",
    tags=["log"],
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


@router.post("/", response_model=list[SchemaLog])
@limiter.limit(LIMIT_VALUE)
async def show_logs(
  request: Request,
  current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
  filters: SchemaLogFilter,
  db: Session = Depends(get_db)
):
  logs = get_logs(db, current_user, filters)

  return logs


@router.get("/charts/line_periods", response_model=SchemaLogChartLinePeriod)
@limiter.limit(LIMIT_VALUE)
async def chart_line_periods(
  request: Request,
  current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
  db: Session = Depends(get_db)
):

  periods = get_last_half_hour(last_minutes=60)

  logs_counts = count_logs_in_time_periods(db, current_user, periods)

  return {
    'periods': list(logs_counts.keys()),
    'total': list(logs_counts.values())
  }


@router.get("/charts/log_total_types", response_model=SchemaLogTypesTotal)
@limiter.limit(LIMIT_VALUE)
async def chart_log_type_total(
  request: Request,
  current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
  db: Session = Depends(get_db)
):

  logs_type_count = total_type_logs_in_period(db, current_user)

  return logs_type_count


@router.get("/charts/log_count_types_period", response_model=SchemaLogChartTypesCountPeriod)
@limiter.limit(LIMIT_VALUE)
async def chart_log_type_count_period(
  request: Request,
  current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
  db: Session = Depends(get_db)
):

  logs_type_count = count_type_logs_in_period(db, current_user)

  return {
    'daily_anomalies': {
      'dates': list(logs_type_count['daily_anomalies'].keys()),
      'count': list(logs_type_count['daily_anomalies'].values()),
    },
    'daily_non_anomalies': {
      'dates': list(logs_type_count['daily_non_anomalies'].keys()),
      'count': list(logs_type_count['daily_non_anomalies'].values()),
    },
  }
