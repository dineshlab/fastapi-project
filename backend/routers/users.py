from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, crud

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = crud.get_user_by_email(db, email=user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = crud.get_user(db, user_id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user
