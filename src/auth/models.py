from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
import pytz

class User(SQLModel, table=True):
    __tablename__ = 'users'
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
        ))# unique - pydantic fields function
    username: str
    email: str
    firstname: str
    lastname: str
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now(pytz.utc)))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now(pytz.utc)))

    def __repr__(self):
        return f'<User {self.username}>'