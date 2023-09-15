from fastapi import FastAPI,  Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..models import models
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/post/all")
async def get_all(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"message": post}


@router.post("/post/new", status_code=status.HTTP_201_CREATED)
def creat_new_post(user_input: models.NewPost, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=user_input.title,
        content=user_input.content,
        published=user_input.published
    )

    db.add(new_post)
    db.commit()
