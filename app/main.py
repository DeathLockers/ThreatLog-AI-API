from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
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
                   http_message_429_exception_handler)

app = FastAPI()

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
