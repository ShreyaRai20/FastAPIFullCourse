# FastAPIFullCourse

Virtual Environment

Create- 
python3 -m venv .venv 

Activate-
source .venv/bin/activate

fastapi
pip install fastapi

uvicorn
pip install uvicorn

pip freeze > requirements.txt

uvicorn main:app --reload
uvicorn src.main:app --reload


uvicorn filename:instance --reload

pip install asyncpg 

pip install sqlmodel

pip install greenlet

pip install alembic

alembic init -t async migrations
migration environment,to store versions/ changes.

alembic revision --autogenerate -m "added hash_password"

alembic upgrade head

pip install passlib

pip install bcrypt

pip install pyjwt


in terminal python3 

import secrets
>>> secrets.token_hex(16)

pip install aioredis

install redis 

brew install redis
brew services start redis
brew services start redis

pip install fastapi_mail

pip install itsdangerous


pip install celery

pip install asgiref

celery -A src.celery_tasks.c_app worker

pip install flower

celery -A src.celery_tasks.c_app flower

pip install pytest


pip install schemathesis

st run http://localhost:8000/openapi.json --experimental=openapi-3.1
ctrl + D
