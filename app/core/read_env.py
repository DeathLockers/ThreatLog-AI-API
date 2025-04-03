import os
from dotenv import load_dotenv

load_dotenv()


def getenv(key: str, default="") -> str:
  return os.getenv(key, default)
