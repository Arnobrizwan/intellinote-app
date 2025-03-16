# app/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an asynchronous engine using the DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker factory for async sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for FastAPI routes to use database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session