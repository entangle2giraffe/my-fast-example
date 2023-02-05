from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud, schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users



@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{email}", response_model=schemas.User)
def update_password(
    email: str, password_update: schemas.UserUpdate, db: Session = Depends(get_db)
):
    # user input old password and new desired password
    return crud.update_password(db=db, password=password_update, email=email)

@router.delete("/{user_id}/{password}")
async def delete_user(user_id: int, password: str, db: Session = Depends(get_db)):
    # delete the entire user
    if password+"notreallyhashed" == crud.get_user(db=db, user_id=user_id).hashed_password:
        return crud.remove_user(db=db, user_id=user_id, password=password)
    else:
        raise HTTPException(status_code=422, detail="Incorrect password")

