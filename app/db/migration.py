from sqlalchemy.exc import SQLAlchemyError
from ..db import engine, Base
from ..seeders import SeederUsers

try:
  Base.metadata.drop_all(bind=engine)
except SQLAlchemyError as e:
  pass

Base.metadata.create_all(bind=engine)

SeederUsers()