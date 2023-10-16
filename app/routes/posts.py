from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..models.post import Post, NewPost, EditPost, PostOut
from ..models.user import User
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from typing import Annotated, List, Any, Dict

router = APIRouter(
    tags=["Post"],
)


@router.get("/posts", status_code=status.HTTP_200_OK, response_model=List[PostOut])
async def get_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    """This function gets the all the posts of the current user.

    Returns:
        List of all the posts of the current user. If user exists or else returns an empty list.
    """
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()

    # Convert created_at to string before passing it to PostOut model
    posts_dict = [post.__dict__ for post in posts]
    for post in posts_dict:
        post["created_at"] = str(post["created_at"])

    return posts_dict


@router.post("/post/new", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def make_new_post(
    post: NewPost,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PostOut:
    """
    Create a new post for the current user.

    Args:
        post (NewPost): The post data to be created.

    Returns:
        PostOut: The newly created post.
    """
    new_post = Post(**post.model_dump(), user_id=current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Convert created_at to string before passing it to PostOut model
    new_post_dict = new_post.__dict__
    new_post_dict["created_at"] = str(new_post_dict["created_at"])

    return PostOut(**new_post_dict)


@router.get("/post/{id}", status_code=status.HTTP_200_OK, response_model=PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    currrent_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    if not post.published and post.user_id != currrent_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to view this post.",
        )

    # Convert created_at to string before passing it to PostOut model
    post_dict = post.__dict__
    post_dict["created_at"] = str(post_dict["created_at"])

    return PostOut(**post_dict)


@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a post with the given id, if the current user has permission to do so.

    Args:
        id (int): The id of the post to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If the post is not found or the current user does not have permission to delete the post.

    Returns:
        None
    """

    post_query = db.query(Post).filter(Post.id == id)

    post: Post | None = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    if post.user_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to delete this post.",
        )

    post_query.delete(synchronize_session=False)

    db.commit()


@router.put("/post/{id}", status_code=status.HTTP_200_OK)
async def edit_post(
    id: int,
    new_data: EditPost,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    post_query = db.query(Post).filter(Post.id == id)

    post: Post | None = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    if post.user_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to edit this post.",
        )

    post_query.update(new_data.model_dump(), synchronize_session=False)  # type: ignore

    db.commit()
