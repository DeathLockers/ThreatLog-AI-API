import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import contextlib

from app.db.database import get_db_async

from .routers import (AuthRouter,
                      LogRouter,
                      VerifiedLogRouter,
                      NotificationRouter,
                      WebsocketRouter)
from .core import (limiter,
                   DOMAINS_ORIGINS_LIST,
                   http_message_exception_handler,
                   http_message_400_exception_handler,
                   http_message_422_exception_handler,
                   http_message_429_exception_handler,
                   )


@asynccontextmanager
async def lifespan(app: FastAPI):
  """Inicializa Kafka on startup"""
  from .core import kafka_consumer
  async with get_db_async() as db:  # Use 'async with' if get_db is async
    kafka_task = asyncio.create_task(kafka_consumer(db))
    await asyncio.sleep(5)
    try:
      yield
    finally:
      kafka_task.cancel()
      with contextlib.suppress(asyncio.CancelledError):
        await kafka_task

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=DOMAINS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=lambda: "global")
app.state.limiter = limiter


@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc: ValueError):
  return await http_message_400_exception_handler(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
  return await http_message_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
  return await http_message_422_exception_handler(request, exc)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_exception_handler(request: Request, exc: RateLimitExceeded):
  return await http_message_429_exception_handler(request, exc)

app.include_router(AuthRouter)
app.include_router(LogRouter)
app.include_router(VerifiedLogRouter)
app.include_router(NotificationRouter)
app.include_router(WebsocketRouter)
