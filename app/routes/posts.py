from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..models.post import Post, NewPost, EditPost, PostOut
from ..models.user import User
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from typing import List, Annotated

router = APIRouter(
    tags=["Post"],
)


@router.get("/posts", status_code=status.HTTP_200_OK, response_model=List[PostOut])
async def get_posts(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    limit: int = 10,
    title_content: str | None = None,
) -> List[PostOut]:
    """This function gets the number of posts of the current user.

    Returns:
        List of all the posts of the current user. If user exists or else returns an empty list.
    """
    if not title_content:
        posts = (
            db.query(Post).filter(Post.user_id == current_user.id).limit(limit).all()
        )
    else:
        posts = (
            db.query(Post)
            .filter(Post.user_id == current_user.id)
            .filter(Post.title.contains(title_content))
            .limit(limit)
            .all()
        )


    output: List[PostOut] = [post for post in posts]

    if not output:
        meassage = "."
        if title_content != "":
            meassage = f" with {title_content} in title."

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found{meassage}",
        )

    return output



@router.post("/post/new", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def make_new_post(
    post: NewPost,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
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

    return new_post



@router.get("/post/{id}", status_code=status.HTTP_200_OK, response_model=PostOut)
async def get_post(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> PostOut:
    post = (
        db.query(Post)
        .filter(
            Post.id == id, (Post.published == True) | (Post.user_id == current_user.id)
        )
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    if not post.published and post.user_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to view this post.",
        )

    return post



@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
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
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
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
