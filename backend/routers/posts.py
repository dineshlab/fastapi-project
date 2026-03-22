from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import database, schemas, crud, oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    posts = crud.get_posts(db, skip=skip, limit=limit, search=search)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    return crud.create_post(db, post=post, user_id=current_user.id)

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    post = crud.get_post(db, post_id=id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    success = crud.delete_post(db, post_id=id, user_id=current_user.id)
    if success is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return None

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    updated_post = crud.update_post(db, post_id=id, post=post, user_id=current_user.id)
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return updated_post

@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    return crud.vote_post(db, vote=vote, user_id=current_user.id)
