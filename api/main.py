from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import time

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="urvish4503",
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
        cursor = conn.cursor()
        print(
            """
    /ᐠ_ ꞈ _ᐟ\\
    """
        )
        break
    except Exception as err:
        print(f"{err}, connection failed.")
        time.sleep(2)


class User(BaseModel):
    name: str
    is_awesome: bool


class Post(BaseModel):
    id: int | None = None
    title: str
    content: str
    is_public: bool = True
    name: str | None = None
    rating: int | None = None


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/post")
def get_post():
    cursor.execute("""select * from posts where id < 9""")
    post = cursor.fetchall()
    return {"data": post}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def new_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.is_public),
    )

    newone = cursor.fetchone()

    conn.commit()

    return {"my new post": newone}


@app.get("/post/{id}", status_code=status.HTTP_200_OK)
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


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.put("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def edit_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, id),
    )

    updated_post = cursor.fetchone()

    if not updated_post:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    conn.commit()
