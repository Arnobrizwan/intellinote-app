from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
import uuid

# User schemas

# Schema for user registration
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for user login (only requires email and password)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for user output (what’s returned from the API)
class UserOut(BaseModel):
    user_id: uuid.UUID
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# JWT schemas

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

# Note schemas

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteOut(NoteBase):
    note_id: uuid.UUID
    summary: Optional[str] = None
    keywords: Optional[str] = None
    sentiment: Optional[str] = None
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True