from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class User(BaseModel):
    name: str
    is_awesome: bool


class Post(BaseModel):
    uid: int
    title: str
    content: str
    name: str
    is_public: bool = False
    rating: int = 1


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


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/post")
def new_post(post: Post):
    post_dict = post.model_dump()
    post_dict["uid"] = randrange(20, 4039)
    my_posts.append(post_dict)
    return HTTPException(status_code=status.HTTP_200_OK)


@app.get("/post/latest")
def last_post():
    return my_posts[len(my_posts) - 1]


@app.get("/post/{id}")
def get_post(id: int):
    for i in my_posts:
        if int(id) == i["uid"]:
            return {"data": i}
    return {"data": "user not found"}
