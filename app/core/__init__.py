from .read_env import getenv
from .hash_password import hash_password, verify_password
from .jwt.config import (SECRET_KEY,
                         ALGORITHM,
                         ACCESS_TOKEN_EXPIRE_MINUTES,
												 TOKEN_TYPE,
                         oauth2_scheme)
from .jwt.current_user import (get_current_active_user,
                               get_current_user_wewbsocket,
                               get_current_token)
from .http_exceptions import (credentials_exception,
                              forbidden_exception,
                              token_expiration_exception)
from .slowapi import limiter, LIMIT_VALUE
from .websocket_connection import ConnectionManager, connection_manager
from .last_half_hour import get_last_half_hour
from .cors import DOMAINS_ORIGINS_LIST
from .http_exception_handler import (http_message_exception_handler,
                                     http_message_422_exception_handler,
                                     http_message_429_exception_handler)
from .kafka import kafka_consumer
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
