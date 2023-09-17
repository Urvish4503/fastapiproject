from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..models import posts
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/post/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(posts.Post).filter(posts.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")

    return {"post": post}


@router.get("/post/all")
async def get_all(db: Session = Depends(get_db)):
    post = db.query(posts.Post).all()
    return {"message": post}


@router.post("/post/new", status_code=status.HTTP_201_CREATED)
def creat_new_post(user_input: posts.NewPost, db: Session = Depends(get_db)):
    new_post = posts.Post(
        title=user_input.title,
        content=user_input.content,
        published=user_input.published
    )

    db.add(new_post)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)
