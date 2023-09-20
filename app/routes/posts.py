from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..models.posts import Post, NewPost
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/post/all")
async def get_all(db: Session = Depends(get_db)):
    post = db.query(Post).all()
    return {"message": post}


@router.post("/post/new", status_code=status.HTTP_201_CREATED)
async def make_new_post(post: NewPost, db: Session = Depends(get_db)):
    new_post = Post(
        title=post.title,
        content=post.content,
        published=post.published,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"new post": new_post}


@router.get("/post/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found."
        )

    return Response(status_code=status.HTTP_200_OK, content={"post": post})


@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found."
        )

    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/post/{id}", status_code=status.HTTP_200_OK)
async def edit_post(id: int, new_data: NewPost, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found."
        )

    post_query.update(new_data.dict(), synchronize_session=False)

    db.commit()

    return {"status": "ok"}
