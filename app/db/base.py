"""SQLAlchemy Base и общие методы для моделей."""

from typing import Any
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, func

# Базовый класс для всех моделей
Base = declarative_base()

class BaseModel(Base):
    """Базовая модель с общими полями."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), 
                       server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), 
                       server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def dict(self, **kwargs) -> dict[str, Any]:
        """Преобразование модели в словарь (совместимость с Pydantic)."""
        return {c.name: getattr(self, c.name) for c.name, c in self.__mapper__.columns.items()}
    
    def __repr__(self) -> str:
        """Строковое представление модели."""
        columns = [c.name for c in self.__mapper__.columns]
        return f"<{self.__class__.__name__}({', '.join(f'{c}={getattr(self, c)!r}' for c in columns[:3])})>"
