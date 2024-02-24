from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# creating pydantic model
class PostBase(BaseModel):
    title: str                      # data validation
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:             #this will convert orm model (sqlalchemy) to pydantic model (pydantic dictionary)
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:             #this will convert orm model (sqlalchemy) to pydantic model (pydantic dictionary)
        orm_mode = True

class UserCreate(BaseModel):
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