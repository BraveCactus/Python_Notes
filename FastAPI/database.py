"""
В данном файле приведен каркас взаимодействия с локальной базой данных через FastAPI
Основные действия
    1) Добавление книг в базу данных
    2) Извлечение книг из базы данных    

Запуск сервера: uvicorn database:app --reload
URL: http://127.0.0.1:8000/docs
"""

from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///./books.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session()as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    author: Mapped[str]

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"success": True}

class BookAddScheme(BaseModel):
    title: str
    author: str

class BookScheme(BookAddScheme):
    id: int

@app.post("/books")
async def add_book(data: BookAddScheme, session: SessionDep):
    new_book = BookModel(
        title = data.title,
        author = data.author,
    )
    session.add(new_book)
    await session.commit()
    return {"success": True}
    
@app.get("/books")
async def get_book(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()

    