from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from src1.config import Config

# Async SQLModel setup 
# async engine for async def
engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    ))

# Database connection with lifespan events 

async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'HELLO';") # SELECT "HELLO"; - will throw error
        result =  await conn.execute(statement)
        print(result.all())

