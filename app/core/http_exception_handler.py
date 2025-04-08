from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse


async def http_message_exception_handler(request: Request, exc: HTTPException):
  if exc.status_code == 401:
    return JSONResponse(
        status_code=401,
        content={"message": "Unauthorized access"}
    )

  if exc.status_code == 403:
    return JSONResponse(
        status_code=403,
        content={"message": "Access not permitted"}
    )

  if exc.status_code == 406:
    return JSONResponse(
      status_code=406,
      content={"message": "Token for email verification has expired"}
    )

  if exc.status_code == 500:
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error, please contact your administrator."}
    )

  # Para otros códigos, simplemente pasamos la excepción
  return request.app.default_exception_handler(request, exc)


async def http_message_422_exception_handler(request: Request, exc: RequestValidationError):
  return JSONResponse(
      status_code=422,
      content={"message": "The data entered is not valid", "details": exc.errors()}
    )


async def http_message_429_exception_handler(request: Request, exc: RateLimitExceeded):
  return JSONResponse(
      status_code=429,
      content={
          "message": "Too many requests. Please try again later.",
      },
  )
