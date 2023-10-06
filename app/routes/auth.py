from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils import verify
from ..models.user import UserCred

router = APIRouter(prefix="/auth", tags=["Authentication", "Login", "Signup"])


@router.post("/login")
def login(user_cred: UserCred, db: Session = Depends(get_db)):
    user = db.query()
