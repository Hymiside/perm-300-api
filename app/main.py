from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.utils import service

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/news")
async def news():
    try:
        response_news = service.get_news()
        if not response_news:
            while True:
                response_news = service.get_news()
                if response_news:
                    break
        return JSONResponse(status_code=200, content=response_news)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/posts")
async def posts():
    try:
        response_posts = service.get_posts()
        if not response_posts:
            while True:
                response_posts = service.get_posts()
                if response_posts:
                    break
        return JSONResponse(status_code=200, content=response_posts)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
