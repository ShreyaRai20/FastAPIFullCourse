from fastapi import FastAPI
from src.books.routes import book_router

version ='v2'

app = FastAPI(
    title='bookly',
    description='A RestAPI for book review webservice',
    version=version
)

app.include_router(book_router, prefix=f'/api/{version}/books', tags=['books'])


# ORM - translates between a programming language such as python and database like postgres
# Mapping Object to Tables - create python classes to represent tables in the database. each object of these classes corresponds to a row in the batabase table.
# Interacts with Data - you can then interact with these python pbjects as if they were regular ojects as if they wee regular objects in your code, like setting attributes and calling methods.
# Behinds the Scenes - crud performed ORM translates it to specific sql statement for the database
# SQLAlchemy is used to perform this operations

