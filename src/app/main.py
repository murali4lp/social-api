from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from . import models
from .database import engine
from .routers import post as post_routes, user as user_routes, auth as auth_routes, vote as vote_routes

# No longer needed after alembic setup
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_routes.router)
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(vote_routes.router)


@app.get("/")
def root():
    return {"message": "Hello World"}



