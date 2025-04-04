from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from .routers import (AuthRouter, LogRouter, VerifiedLogRouter, WebsocketRouter)
from .core import limiter

app = FastAPI()


app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.include_router(AuthRouter)
app.include_router(LogRouter)
app.include_router(VerifiedLogRouter)
app.include_router(WebsocketRouter)
