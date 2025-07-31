
import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
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

@app.get("/{full_path:path}")
def unknown(full_path: str):
    with open("notFound.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")

class PostModel(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime.datetime

post_list: List[PostModel] = []

def serialized_posts():
    posts_serialized = []
    for post in post_list:
        posts_serialized.append(post.model_dump_json())
    return posts_serialized

@app.post("/posts")
def add_players(new_post: List[PostModel]):
    post_list.extend(new_post)
    return JSONResponse( {"posts": serialized_posts()}, status_code=201)
