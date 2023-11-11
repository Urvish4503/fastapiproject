from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel

from ..database import Base


class Votes(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    is_reacted = Column(Boolean, nullable=False)

    is_like = Column(Boolean, nullable=False)
    is_dislike = Column(Boolean, nullable=False)

    owner = relationship("User")
    post = relationship("Post", back_populates="likes")


class Reactions(BaseModel):
    post_id: int
