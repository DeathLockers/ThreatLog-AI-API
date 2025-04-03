from fastapi.security import OAuth2PasswordBearer
from ...core import getenv

SECRET_KEY = getenv("JWT_SECRET_KEY")
ALGORITHM = getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
