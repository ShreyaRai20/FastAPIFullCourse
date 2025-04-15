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

