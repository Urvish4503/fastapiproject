from fastapi import FastAPI
from .routes import posts, users
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
