import uuid
from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field, ConfigDict


class ShowBook(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: uuid.UUID
    title: Annotated[str, Field(max_length=500)]
    author: Annotated[str, Field(max_length=300)]
    year: Annotated[int, Field(ge=1000, le=datetime.now().year)]
    genre: Annotated[str, Field(max_length=100)]
    pages: Annotated[int, Field(gt=0)]
    available: bool = True
    isbn: str | None = None
    description: str | None = None
    extra: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime