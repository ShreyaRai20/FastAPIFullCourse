# forms on frontend

from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class UserCreateModel(BaseModel):
    firstname: str = Field(max_length=25)
    lastname: str = Field(max_length=25)
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    uid : uuid.UUID
    username: str
    email: str
    firstname: str
    lastname: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime 
    updated_at: datetime 

