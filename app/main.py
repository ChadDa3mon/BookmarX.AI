from fastapi import FastAPI, Path
from pydantic import BaseModel
from models import Bookmark,BookmarxResponse,BookmarxListResponse, URLAlreadyExistsError
from typing import List
from utils import add_bookmark,get_all_bookmarx,get_bookmarx_by_id
from exceptions import URLAlreadyExistsError#, WriteArticleToDBError


app = FastAPI()

@app.get("/bookmarx",response_model=BookmarxListResponse)
#@app.get("/bookmarx")
async def get_bookmarks():
    bookmark_list = get_all_bookmarx()
    for bookmarx in bookmark_list:
        print(f"Bookmark: {bookmarx}")
        print(f" ID Type: {type(bookmarx['id'])}")
        print(f" URL Type: {type(bookmarx['url'])}")
        print(f" Summary Type: {type(bookmarx['summary'])}")
    return BookmarxListResponse(bookmarx = bookmark_list)

@app.get("/bookmarx/{id}", response_model=BookmarxResponse)
async def get_bookmarx(id: int = Path(..., title="Bookmark ID")):
    bookmark = get_bookmarx_by_id(id)
    if bookmark is None:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@app.post("/bookmarks/add")
async def add_bookmark_route(payload: Bookmark):
    url = str(payload.url)
    # print(f"Received URL: {url}")
    
    try:
        await add_bookmark(url)
    except URLAlreadyExistsError as e:
        return {"message": str(e)}
    # except WriteArticleToDBError as e:
    #     return {"message": str(e)}
    except Exception:
        return {"message": "An unknown error occurred"}
    
    return {"message": "Bookmark added successfully"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
