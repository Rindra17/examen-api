
import datetime
from operator import truediv
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

app = FastAPI()

@app.get("/ping")
def ping():
    return {"pong"}


@app.get("/home")
def home():
    with open("home.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")


class PostModel(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime.datetime

post_list: List[PostModel] = []

def serialized_posts():
    posts_serialized = []
    for post in post_list:
        post.creation_datetime = datetime.datetime.__str__(post.creation_datetime)
        posts_serialized.append(post.model_dump())
    return posts_serialized

@app.post("/posts")
def add_posts(new_post: List[PostModel]):
    post_list.extend(new_post)
    return JSONResponse( {"posts": serialized_posts()}, status_code=201)

@app.get("/posts")
def get_posts():
    return JSONResponse( {"posts": serialized_posts()}, status_code=200)

@app.get("/ping/auth")
def get_ping_auth(request: Request):
    authentification = request.headers.get("Accept")
    if authentification is None:
        return JSONResponse({"message": "n'est pas autorisé"}, status_code=401)
    if authentification != "123456":
        return JSONResponse({"message": "vous n'avez pas les permissions nécessaires"}, status_code=403)
    return JSONResponse({"players": "pong"})

@app.get("/{full_path:path}")
def unknown(full_path: str):
    with open("notFound.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")
