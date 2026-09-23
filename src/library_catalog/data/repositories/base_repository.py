from typing import Generic, TypeVar, Type
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
    
    async def create(self, **kwargs) -> T:
        """Создать запись."""
        instance = self.model(**kwargs)

        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
        except Exception:
            await self.session.rollback()
            raise
        
        return instance
    
    async def get_by_id(self, id: UUID) -> T | None:
        """
        Получить по ID.
        """
        result = await self.session.get(self.model, id)
        return result
    
    async def update(self, id: UUID, **kwargs) -> T | None:
        """Обновить запись."""
        instance = await self.get_by_id(id)

        if not instance:
            return None
        
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
                
        try:
            await self.session.commit()
            await self.session.refresh(instance)
        except Exception:
            await self.session.rollback()
            raise
        
        return instance
    
    async def delete(self, id: UUID) -> bool:
        """Удалить запись."""
        instance = await self.get_by_id(id)

        if instance:
            await self.session.delete(instance)
            try:
                await self.session.commit()
            except Exception:
                await self.session.rollback()
                raise
            
            return True
        
        return False
        
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[T]:
        """Получить все записи с пагинацией."""
        query = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
