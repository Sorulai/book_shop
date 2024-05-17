from pydantic import BaseModel, UUID4, ConfigDict, Field


class BookCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    author: str
    year: int
    genre: str
    user_id: UUID4


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author: str
    year: int
    genre: str
    user_id: UUID4


class BookUpdate(BaseModel):
    title: str = None
    author: str = None
    year: int = None
    genre: str = None
