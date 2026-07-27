from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import setting

# create an engine instance and keep a reference to it
engine = create_async_engine(
    url=setting.DATABASE_URL,
    echo=True,
)


async def create_db_tables():
    async with engine.begin() as connection: 
        from .models import Shipment
        await connection.run_sync(SQLModel.metadata.create_all(bind=engine))
        

def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]