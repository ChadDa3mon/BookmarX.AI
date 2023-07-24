from fastapi import FastAPI
from pydantic import BaseModel
from models import Bookmark
from typing import List
from utils import add_bookmark


bookmarks = []

app = FastAPI()

@app.get("/bookmarks")
async def get_bookmarks():
    return bookmarks

@app.post("/bookmarks/add")
async def add_bookmark_route(payload: Bookmark):
    url = str(payload.url)
    print(f"Received URL: {url}")
    results = await add_bookmark(url)
    if "URL Already Exists" in results:
        return {"message": "URL already exists"}
    

    return {"message": "Bookmark added successfully"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
