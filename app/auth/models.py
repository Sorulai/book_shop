import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    books = relationship("Book", back_populates="user")
