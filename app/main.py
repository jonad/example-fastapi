from fastapi import FastAPI
from .database import engine
from . import models  # import the Pydantic model for posts
from .routers import post, user, auth, vote  # import the routers for posts and users
from fastapi.middleware.cors import CORSMiddleware  # import CORS middleware

# models.Base.metadata.create_all(engine)  # create database tables

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,  # add CORS middleware to the FastAPI app
    allow_origins=origins,  # allow all origins
    allow_credentials=True,  # allow credentials
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

app.include_router(post.router)  # include the post router
app.include_router(user.router)  # include the user router
app.include_router(auth.router)  # include the auth router
app.include_router(vote.router)  # include the vote router


@app.get("/")  # decorator to define a GET endpoint at the root path
async def read_root():  # use async def for asynchronous support
    """
    Root endpoint that returns a simple greeting message.
    """
    return {"message": "Hello, World!"}
