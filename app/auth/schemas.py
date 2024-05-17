import uuid
from typing import Union

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str = Field(pattern=r"^[а-яА-Яa-zA-Z\-]+$")
    surname: str = Field(pattern=r"^[а-яА-Яa-zA-Z\-]+$")
    email: EmailStr
    password: str


class DeleteUserResponse(BaseModel):
    user_id: uuid.UUID


class UpdateUserResponse(BaseModel):
    user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    name: Union[str, None] = Field(None, pattern=r"^[а-яА-Яa-zA-Z\-]+$")
    surname: Union[str, None] = Field(None, pattern=r"^[а-яА-Яa-zA-Z\-]+$")
    email: Union[EmailStr, None] = Field(None)
