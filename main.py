from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from typing import Optional, List
from pydantic import BaseModel
from fastapi import Header

app = FastAPI()

# basic web server
@app.get('/')
async def read_root():
    return {'message': 'Hello World!'}

# Path parameters - dynamic
# @app.get('/greet/{name}')
# async def greet_name(name: str) -> dict:
#     return {'message': f'Hello {name}!'}

# query parameter
# /greet?name=shreya
# @app.get('/greet')
# async def greet_name(name: str) -> dict:
#     return {'message': f'Hello {name}!'}


# Path parameters + query parameter
@app.get('/greet/{name}')
async def greet_name(name: str, age:int) -> dict:
    return {'message': f'Hello {name}! , with age {age}'}


# Optional parameter - typing
@app.get('/greet')
async def greet_name(  age: int, name: Optional[str] = 'User') -> dict:
    return {'message': f'Hello {name}! , with age {age}'}


# Request Body
# serializer/schema - validate the data

class BookCreateModel(BaseModel):
    title : str
    auther :  str


@app.post('/create_book')
async def create_book(book_data: BookCreateModel):
    return book_data

# Reading and setting headers  

@app.get('/get_headers', status_code=500)
async def get_header(
    accept: str =  Header(None),
    content_type: str =  Header(None),
    user_agent: str =  Header(None),
    host: str =  Header(None),
    ):

    request_headers = {}
    request_headers['Accept'] = accept
    request_headers['Content_type'] = content_type
    request_headers['User_Agent'] = user_agent
    request_headers['Host'] = host

    return request_headers

# Build a REST API on a Python List  
# CRUD, Resource - the data that an API provides or allows us to manipulate. This is accessible through an endpoint

books = [
  {
    "id": 1,
    "title": "Think Python",
    "author": "Allen B. Downey",
    "publisher": "O'Reilly Media",
    "published_date": "2021-01-01",
    "page_count": 1234,
    "language": "English"
  },
  {
    "id": 2,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "publisher": "Prentice Hall",
    "published_date": "2008-08-11",
    "page_count": 464,
    "language": "English"
  },
  {
    "id": 3,
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt and David Thomas",
    "publisher": "Addison-Wesley",
    "published_date": "1999-10-30",
    "page_count": 352,
    "language": "English"
  },
  {
    "id": 4,
    "title": "Introduction to the Theory of Computation",
    "author": "Michael Sipser",
    "publisher": "Cengage Learning",
    "published_date": "2012-06-27",
    "page_count": 504,
    "language": "English"
  },
  {
    "id": 5,
    "title": "Python Crash Course",
    "author": "Eric Matthes",
    "publisher": "No Starch Press",
    "published_date": "2015-11-01",
    "page_count": 544,
    "language": "English"
  },
  {
    "id": 6,
    "title": "Design Patterns",
    "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
    "publisher": "Addison-Wesley Professional",
    "published_date": "1994-10-31",
    "page_count": 395,
    "language": "English"
  },
  {
    "id": 7,
    "title": "Artificial Intelligence: A Modern Approach",
    "author": "Stuart Russell and Peter Norvig",
    "publisher": "Pearson",
    "published_date": "2020-04-28",
    "page_count": 1152,
    "language": "English"
  },
  {
    "id": 8,
    "title": "Fluent Python",
    "author": "Luciano Ramalho",
    "publisher": "O'Reilly Media",
    "published_date": "2015-08-20",
    "page_count": 792,
    "language": "English"
  },
  {
    "id": 9,
    "title": "Deep Learning with Python",
    "author": "François Chollet",
    "publisher": "Manning Publications",
    "published_date": "2017-10-28",
    "page_count": 384,
    "language": "English"
  },
  {
    "id": 10,
    "title": "Automate the Boring Stuff with Python",
    "author": "Al Sweigart",
    "publisher": "No Starch Press",
    "published_date": "2015-04-14",
    "page_count": 504,
    "language": "English"
  }
]


class Book(BaseModel):
    id : int
    title : str
    author : str
    publisher : str
    published_date : str
    page_count : int
    language : str

class updateBook(BaseModel):
    title : str
    author : str
    publisher : str
    published_date : str
    page_count : int
    language : str


# Read - get all books
@app.get('/books', response_model=List[Book])
async def get_books():
    return books


# Create - create a book
@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

# Read - get a book
@app.post('/books/{book_id}')
async def get_books(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found')

# Update - update a book
@app.patch('/books/{book_id}')
async def update_a_book(book_id: int, updated_book: updateBook) -> dict:
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
@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found')
