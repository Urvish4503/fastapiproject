from sqlalchemy import Integer, String, Boolean, Column, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
from pydantic import BaseModel


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: str
    user_id: str


class NewPost(BaseModel):
    title: str
    content: str
    published: bool = True


class EditPost(BaseModel):
    title: str
    content: str
