from fastapi import FastAPI
from .routes import posts
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
