from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config

# Async SQLModel setup 
# async engine for async def
async_engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        # echo=True 
    ))

# Database connection with lifespan events 

async def init_db():
    async with async_engine.begin() as conn:
        # statement = text("SELECT 'HELLO';")
        # result = await conn.execute(statement)
        # return statement
        from src.db.models import Books
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session
    

