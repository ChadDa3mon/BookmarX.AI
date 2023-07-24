from fastapi import FastAPI
from pydantic import BaseModel
from models import Bookmark
from typing import List
from utils import add_bookmark
from exceptions import URLAlreadyExistsError, WriteArticleToDBError

bookmarks = []

app = FastAPI()

@app.get("/bookmarks")
async def get_bookmarks():
    return bookmarks

@app.post("/bookmarks/add")
async def add_bookmark_route(payload: Bookmark):
    url = str(payload.url)
    print(f"Received URL: {url}")
    
    try:
        await add_bookmark(url)
    except URLAlreadyExistsError as e:
        return {"message": str(e)}
    except WriteArticleToDBError as e:
        return {"message": str(e)}
    except Exception:
        return {"message": "An unknown error occurred"}
    
    return {"message": "Bookmark added successfully"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
