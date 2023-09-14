from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from main import conn, cursor

router = FastAPI()


@router.get("/")
def root():
    return {"message": "Hello World"}


@router.get("/temp")
def temp(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"message": post}


@router.get("/post")
def get_post():
    cursor.execute("""select * from posts where id < 9""")
    post = cursor.fetchall()
    return {"data": post}


@router.get("/post/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    cursor.execute(
        """SELECT * FROM posts where id = %s""",
        (str(id)),
    )

    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"a post with id: {id} does not exists.",
        )

    return {"post": post}


@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        cursor.execute(
            """DELETE FROM posts WHERE id = %s RETURNING *""",
            (id,),
        )
        deleted_post = cursor.fetchone()

        if not deleted_post:
            raise Response(status_code=status.HTTP_404_NOT_FOUND)

        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        raise Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @router.put("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def edit_post(id: int, post: Post):
#     cursor.execute(
#         """UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""",
#         (post.title, post.content, id),
#     )

#     updated_post = cursor.fetchone()

#     if not updated_post:
#         return Response(status_code=status.HTTP_404_NOT_FOUND)

#     conn.commit()

# @router.post("/post", status_code=status.HTTP_201_CREATED)
# def new_post(post: Post):
#     cursor.execute(
#         """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
#         (post.title, post.content, post.is_public),
#     )

#     newone = cursor.fetchone()

#     conn.commit()

#     return {"my new post": newone}
