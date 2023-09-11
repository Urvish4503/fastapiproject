from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
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


# @app.get("/post/latest")
# def last_post():
#     if len(my_posts) == 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return my_posts[len(my_posts) - 1]


# @app.get("/post/{id}", status_code=status.HTTP_200_OK)
# def get_post(id: int):
#     for i in my_posts:
#         if int(id) == i["uid"]:
#             return {"data": i}
#     return Response(status_code=status.HTTP_404_NOT_FOUND)


# @app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     inx = user_index(id)
#     if inx > -1:
#         my_posts.pop(inx)
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#     return Response(status_code=status.HTTP_404_NOT_FOUND)


# @app.put("/post/{id}")
# def change_post(id: int, post: Post):
#     inx = user_index(id)

#     if inx == -1:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with {id} does not exist.",
#         )

#     temp = post.model_dump()
#     temp["uid"] = id
#     my_posts[inx]["title"] = temp["title"]
#     my_posts[inx]["content"] = temp["content"]
#     return {
#         "data": temp,
#     }
