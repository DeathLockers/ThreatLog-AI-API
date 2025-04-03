from sqlalchemy.orm import Session
from ..models import User as ModelUser


def get_user(db: Session, user_id: str):
  return db.query(ModelUser).filter(ModelUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
  return db.query(ModelUser).filter(ModelUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(ModelUser).order_by(ModelUser.name).offset(skip).limit(limit).all()
