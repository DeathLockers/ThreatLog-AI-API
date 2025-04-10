import asyncio
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from requests import Session
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.db.database import get_db

from .routers import (AuthRouter, LogRouter, VerifiedLogRouter, WebsocketRouter)
from .core import (limiter,
                   DOMAINS_ORIGINS_LIST,
                   http_message_exception_handler,
                   http_message_422_exception_handler,
                   http_message_429_exception_handler,
                   )


@asynccontextmanager
async def lifespan(app: FastAPI):
  """Inicializa gestor de conexiones"""
  from .core import kafka_consumer
  kafka_task = asyncio.create_task(kafka_consumer(get_db))
  yield
  kafka_task.cancel()

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
app.include_router(WebsocketRouter)
