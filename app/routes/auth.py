from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import get_db
from ..utils import verify
from ..models.user import User
from ..oauth2 import create_access_token

router = APIRouter(
    tags=["Authentication"],
)


@router.post("/login")
def login(
    user_cred: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    This will check the email and password.
    If both is correct then it will give a JWT back.
    """
    user = db.query(User).filter(User.email == user_cred.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found with this email.",
        )

    if not verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password",
        )

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
