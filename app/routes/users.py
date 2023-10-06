from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..models.user import User, NewUser, UserOut
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    tags=["User"],
)


@router.post("/user/new", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def creat_user(user: NewUser, db: Session = Depends(get_db)):
    """
    Creates a new user.

    Raises:
        HTTPException: Raised if a user with the same email already exists.

    Returns:
        UserOut: The newly created user.
    """
    new_user = User(**user.model_dump())

    is_in = db.query(User).filter(User.email == new_user.email).first()

    if is_in:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this same email.",
        )

    try:
        hashed_password = utils.hash(user.password)
        new_user.password = hashed_password
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
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return user
