from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import register_all_errors
from .middleware import register_middleware

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f'server is starting ... ')
    await init_db()
    yield
    print(f'server has been stopped')

version ='v1'

app = FastAPI(
    title='bookly',
    description='A RestAPI for book review webservice',
    version=version,
    contact={'email':'shreya200199@gmail.com'}

    # lifespan=life_span
)

register_all_errors(app)
register_middleware(app)

app.include_router(book_router, prefix=f'/api/{version}/books', tags=['books'])
app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['auth'])
app.include_router(review_router, prefix=f'/api/{version}/reviews', tags=['reviews'])
app.include_router(tags_router, prefix=f'/api/{version}/tags', tags=['tags'])


# ORM - translates between a programming language such as python and database like postgres
# Mapping Object to Tables - create python classes to represent tables in the database. each object of these classes corresponds to a row in the batabase table.
# Interacts with Data - you can then interact with these python pbjects as if they were regular ojects as if they wee regular objects in your code, like setting attributes and calling methods.
# Behinds the Scenes - crud performed ORM translates it to specific sql statement for the database
# SQLAlchemy is used to perform this operations

