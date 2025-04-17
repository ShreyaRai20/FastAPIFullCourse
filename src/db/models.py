from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, date
import pytz
from typing import List, Optional

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
    role: str = Field(sa_column= Column(pg.VARCHAR, nullable=False, server_default='user'))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now(pytz.utc)))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now(pytz.utc)))
    books: List['Books'] = Relationship(back_populates='user', sa_relationship_kwargs={'lazy':'selectin'})
    reviews: List['Review'] = Relationship(back_populates='user', sa_relationship_kwargs={'lazy':'selectin'})

    def __repr__(self):
        return f'<User {self.username}>'
    

# sql model
class Books(SQLModel, table=True):
    __tablename__ = "books"
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
        ))# unique - pydantic fields function
    title : str
    author : str
    publisher : str
    published_date : date
    page_count : int
    language : str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key='users.uid')
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now(pytz.utc)))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now(pytz.utc)))
    user: Optional['User'] = Relationship(back_populates='books')
    reviews: List['Review'] = Relationship(back_populates='book', sa_relationship_kwargs={'lazy':'selectin'})

    def __repr__(self):
        return f'<Book {self.title}>'
    

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
        ))# unique - pydantic fields function
    rating: int = Field(lt=5)
    review_text : str 
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key='users.uid')
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key='books.uid')
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now(pytz.utc)))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now(pytz.utc)))
    user: Optional['User'] = Relationship(back_populates='reviews')
    book: Optional['Books'] = Relationship(back_populates='reviews')

    def __repr__(self):
        return f'<Review for book {self.book_uid}>'
    