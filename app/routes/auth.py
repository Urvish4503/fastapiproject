from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import get_db
from ..utils import verify
from ..models.user import User
from ..models.token import Token
from ..oauth2 import create_access_token

router = APIRouter(
    tags=["Authentication"],
)


@router.post("/login", response_model=Token)
def login(
    user_cred: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token | None:
    """
    Authenticate user credentials and return a JWT access token if successful.

    Args:
        user_cred (OAuth2PasswordRequestForm): The user's email and password.

    Raises:
        HTTPException: If the email or password is incorrect.

    Returns:
        Token: A JWT access token.
    """
    user = db.query(User).filter(User.email == user_cred.username).first()

    # verfiying the user's email.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No user found with this email.",
        )

    # verifying the user's password.
    if not verify(user_cred.password, str(user.password)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong password",
        )

    # making the user.id a string because PyJWT only accepts strings and its type is uuid.UUID.
    access_token: Token = create_access_token(data={"user_id": str(user.id)})

    return access_token
