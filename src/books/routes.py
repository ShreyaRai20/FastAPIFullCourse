from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from uuid import UUID

book_router = APIRouter()
book_service = BookService()

# Build a CRUD REST API on a Python List  
# CRUD, Resource - the data that an API provides or allows us to manipulate. This is accessible through an endpoint
# Organizing API Paths with Routers  

# Read - get all books
@book_router.get('/', response_model=List[Book])
async def get_books(session:AsyncSession=Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


# Create - create a book
@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data:BookCreateModel, session:AsyncSession=Depends(get_session)) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book

# Read - get a book
@book_router.get('/{book_uid}', response_model=Book)
async def get_a_book(book_uid: UUID, session:AsyncSession=Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found')

# Update - update a book
@book_router.patch('/{book_uid}', response_model=Book)
async def update_a_book(book_uid: UUID, 
                        book_update_data: BookUpdateModel, 
                        session:AsyncSession=Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found yes')
    else:
        return updated_book


# Delete - delete a book - confusing revisit
@book_router.delete('/{book_uid}')
async def delete_a_book(book_uid: UUID, session:AsyncSession=Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found to delete')
    else:
        return {}

