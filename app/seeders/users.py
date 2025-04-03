import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..db import engine
from ..core import hash_password
from ..models import User as ModelUser
from ..schemas import UserCreateSeeder as SchemaUserCreateSeeder


def generate_seeder() -> None:
  with open("./app/seeders/data/users.json", encoding="UTF-8") as json_file:

    for user in json.load(json_file):

      user_hashed_password = user["hashed_password"]
      del user["hashed_password"]

      user = SchemaUserCreateSeeder(**user, hashed_password=hash_password(user_hashed_password))

      with Session(engine) as db:
        db_user = ModelUser(**user.model_dump())
        db.add(db_user)

        try:
          db.commit()
        except SQLAlchemyError:
          pass
          # 1062, Duplicate entry

    json_file.close()
