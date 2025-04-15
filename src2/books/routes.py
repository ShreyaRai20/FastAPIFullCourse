from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
# from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel


book_router = APIRouter()



# Build a CRUD REST API on a Python List  
# CRUD, Resource - the data that an API provides or allows us to manipulate. This is accessible through an endpoint
# Organizing API Paths with Routers  

# Read - get all books
@book_router.get('/', response_model=List[Book])
async def get_books():
    return books


# Create - create a book
@book_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

# Read - get a book
@book_router.post('/{book_id}')
async def get_books(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found')

# Update - update a book
@book_router.patch('/{book_id}')
async def update_a_book(book_id: int, updated_book: BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = updated_book.title
            book['author'] = updated_book.author
            book['publisher'] = updated_book.publisher
            book['published_date'] = updated_book.published_date
            book['page_count'] = updated_book.page_count
            book['language'] = updated_book.language
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found')


# Delete - delete a book
@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found')

