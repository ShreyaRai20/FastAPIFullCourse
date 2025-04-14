from sqlmodel import create_engine, text, SQLModel
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
        from src1.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)



