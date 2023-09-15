from fastapi import FastAPI,  Response, status, HTTPException, Depends, APIRouter
from ..db.database import get_db
from ..models import models
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/temp")
def temp(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"message": post}

