from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..models.user import User, NewUser, UserOut
from sqlalchemy.orm import Session
from passlib.context import CryptContext


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/user/new", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def creat_user(user: NewUser, db: Session = Depends(get_db)):
    new_user = User(**user.model_dump())
    is_in = db.query(User).filter(User.email == new_user.email).first()

    if is_in:
        raise HTTPException(
            status_code=409, detail="User already exists with this same email."
        )

    try:
        hashed_password = pwd_context.hash(user.password)
        new_user.password = hashed_password
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(
            status_code=409, detail="User already exists with this same email."
        )
    else:
        return new_user
