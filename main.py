from fastapi import FastAPI
from typing import Optional

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