from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class User(BaseModel):
    name: str
    is_awesome: bool


class Post(BaseModel):
    uid: int | None = None
    title: str
    content: str
    is_public: bool = False
    name: str | None = None
    rating: int | None = None


my_posts = [
    {
        "uid": 12,
        "title": "Title 1",
        "content": "Cute cats",
        "name": "baba",
        "is_public": False,
        "rating": 2,
    },
    {
        "uid": 13,
        "title": "Title 2",
        "content": "Cute dogos",
        "name": "bobo",
        "is_public": True,
        "rating": 1000,
    },
]


def user_index(key: int) -> int:
    for i, j in enumerate(my_posts):
        if j["uid"] == key:
            return i
    return -1


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def new_post(post: Post):
    post_dict = post.model_dump()
    post_dict["uid"] = randrange(20, 4039)
    my_posts.append(post_dict)


@app.get("/post/latest")
def last_post():
    if len(my_posts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return my_posts[len(my_posts) - 1]


@app.get("/post/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    for i in my_posts:
        if int(id) == i["uid"]:
            return {"data": i}
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    inx = user_index(id)
    if inx > -1:
        my_posts.pop(inx)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.put("/post/{id}")
def change_post(id: int, post: Post):
    inx = user_index(id)

    if inx == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not exist.",
        )

    temp = post.model_dump()
    temp["uid"] = id
    my_posts[inx]["title"] = temp["title"]
    my_posts[inx]["content"] = temp["content"]
    return {
        "data": temp,
    }
