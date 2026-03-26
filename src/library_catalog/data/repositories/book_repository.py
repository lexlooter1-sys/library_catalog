from sqlalchemy import select, func, and_
from base_repository import BaseRepository
from ..models.book import Book
from sqlalchemy.ext.asyncio import AsyncSession


class BookRepository(BaseRepository[Book]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)
    
    async def find_by_filters(
        self,
        title: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        year: int | None = None,
        available: bool | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Book]:
        """Поиск книг с фильтрацией."""
        query = select(self.model)
        
        if title:
            query = query.where(self.model.title.ilike(f"%{title}%"))
        if author:
            query = query.where(self.model.author.ilike(f"%{author}%"))
        if genre:
            query = query.where(self.model.genre.ilike(f"%{genre}%"))
        if year is not None:
            query = query.where(self.model.year == year)
        if available is not None:
            query = query.where(self.model.available == available)

        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def find_by_isbn(self, isbn: str) -> Book | None:
        """Найти книгу по ISBN."""
        query = select(self.model).where(self.model.isbn == isbn)
        result = await self.session.scalar(query)
        return result
    
    async def count_by_filters(
        self,
        title: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        year: int | None = None,
        available: bool | None = None,
    ) -> int:
        """Подсчитать количество книг по фильтрам."""
        query = select(func.count(self.model.book_id))
        
        if title:
            query = query.where(self.model.title.ilike(f"%{title}%"))
        if author:
            query = query.where(self.model.author.ilike(f"%{author}%"))
        if genre:
            query = query.where(self.model.genre.ilike(f"%{genre}%"))
        if year is not None:
            query = query.where(self.model.year == year)
        if available is not None:
            query = query.where(self.model.available == available)
            
        result = await self.session.scalar(query)
        return result
        
