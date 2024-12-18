from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True


class CreatePost(PostBase):
    pass


class CreatedUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: CreatedUser
    
    class Config:
        orm_mode = True

class PostVotes(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True
    
class CreateUser(BaseModel):
    email: EmailStr
    password: str
        

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore