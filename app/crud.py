from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(db: Session, password: schemas.UserUpdate, email: str):
    db_user = get_user_by_email(db=db, email=email)

    old_password = password.dict()["old_password"]
    new_password = password.dict()["new_password"]
    if old_password+"notreallyhashed" == db_user.hashed_password:
        db_user.hashed_password = new_password + "notreallyhashed"

        db.commit()
        db.refresh(db_user)
        return db_user

def remove_user(db: Session, user_id: int, password: str):
    db_user = get_user(db=db, user_id=user_id)
    
    db.delete(db_user)
    db.commit()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item