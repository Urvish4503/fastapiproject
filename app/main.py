from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import time
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

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
