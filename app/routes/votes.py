from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from ..oauth2 import get_current_user
from ..database import get_db
from ..models.vote import Votes, Reactions
from ..models.user import User

router = APIRouter()


@router.post("/like", status_code=status.HTTP_201_CREATED)
def like_post(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    post_id: int,
):
    existing_vote = (
        db.query(Votes)
        .filter(Votes.user_id == current_user.id)
        .filter(Votes.post_id == post_id)
        .first()
    )

    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already reacted to this post.",
        )
    else:
        new_vote = Votes(
            user_id=current_user.id,
            post_id=post_id,
            is_reacted=True,
            is_like=True,
            is_dislike=False,
        )
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote
