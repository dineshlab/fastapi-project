from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Post Schemas
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    votes: int = 0

    class Config:
        from_attributes = True

# Vote Schema
class Vote(BaseModel):
    post_id: int
    dir: int  # 1 for upvote, 0 for remove vote

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
