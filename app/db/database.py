from contextlib import asynccontextmanager
from ..db import SessionLocal


def get_db():
  Session = SessionLocal()

  try:
      yield Session
  finally:
    Session.close()

@asynccontextmanager
async def get_db_async():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
