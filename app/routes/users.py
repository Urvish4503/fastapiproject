from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated
from ..models.user import User, NewUser, UserOut
from ..database import get_db
from .. import utils

router = APIRouter(
    tags=["User"],
)


@router.post("/user/new", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def creat_user(
    user: NewUser,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Create a new user.

    This function creates a new user with the provided user information. If a user with the same email already exists,
    an HTTPException with status code 409 (Conflict) is raised.

    Args:
        user (NewUser): The user info to be created.

    Raises:
        HTTPException: If there was an issue creating a user.

    Returns:
        UserOut: Newly created user.
    """

    is_in = db.query(User).filter(User.email == user.email).first()

    if is_in:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this same email.",
        )

    new_user = User(**user.model_dump())

    try:
        hashed_password = utils.hash(user.password)
        new_user.password = hashed_password  # type: ignore
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this same email.",
        )
    else:
        return new_user


@router.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(
    id: int,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user
