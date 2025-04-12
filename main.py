from fastapi import FastAPI, status
from typing import Optional
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



# @app.post('/create_book')
# async def create_book(book_data: BookCreateModel):
#     return book_data

# # Reading and setting headers  

# @app.get('/get_headers', status_code=500)
# async def get_header(
#     accept: str =  Header(None),
#     content_type: str =  Header(None),
#     user_agent: str =  Header(None),
#     host: str =  Header(None),
#     ):

#     request_headers = {}
#     request_headers['Accept'] = accept
#     request_headers['Content_type'] = content_type
#     request_headers['User_Agent'] = user_agent
#     request_headers['Host'] = host

#     return request_headers

