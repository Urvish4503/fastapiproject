from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..models.post import Post, NewPost, EditPost, PostOut
from ..models.user import User
from sqlalchemy.orm import Session
from typing import Any
from ..oauth2 import get_current_user

router = APIRouter(
    tags=["Post"],
)


@router.post("/post/new", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def make_new_post(
    post: NewPost,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    new_post = Post(**post.model_dump(), user_id=current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Convert created_at to string before passing it to PostOut model
    new_post_dict = new_post.__dict__
    new_post_dict["created_at"] = str(new_post_dict["created_at"])

    return PostOut(**new_post_dict)


@router.get("/post/{id}", status_code=status.HTTP_200_OK)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(current_user.id)
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    return post


@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    post = db.query(Post).filter(Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    post.delete(synchronize_session=False)

    db.commit()


# might be useless but I'm keeping it for now.
@router.put("/post/{id}", status_code=status.HTTP_200_OK)
async def edit_post(
    id: int,
    new_data: EditPost,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    post_query = db.query(Post).filter(Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    post_query.update(new_data.model_dump(), synchronize_session=False)  # type: ignore

    db.commit()
