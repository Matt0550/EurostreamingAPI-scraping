import datetime

from fastapi import FastAPI
from typing import Any, List

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from models import Show, ShowsResponse
from functions import EurostreamingWorker


# New response structure: {"details": ..., "status_code": ..., "success": ...}
class ResponseStructure(BaseModel):
    details: Any
    success: bool = True
    status_code: int

# New response class
class CustomResponse(JSONResponse):
    def __init__(self, content: Any, status_code: int = 200, *args, **kwargs):
        # Customize content and pass my new content...
        content = ResponseStructure(details=content, success=False if status_code != 200 else True, status_code=status_code)
        super().__init__(content=content.dict(), status_code=status_code, *args, **kwargs)


app = FastAPI(default_response_class=CustomResponse, title="Eurostreaming Unofficial API", description="An unofficial API for Eurostreaming website", version="1.0.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UP_START_TIME = datetime.datetime.now() # For the uptime

eurostreamingWorker = EurostreamingWorker()
# Handle the 404 error. Use HTTP_exception_handler to handle the error
@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(content={"message": "Not found", "success": False, "code": exc.status_code}, status_code=exc.status_code)
    elif exc.status_code == 405:
        return JSONResponse(content={"message": "Method not allowed", "success": False, "code": exc.status_code}, status_code=exc.status_code)
    else:
        # Just use FastAPI's built-in handler for other errors
        return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    status_code = 422
    print(exc.errors())

    if exc.errors()[0]["type"] == "value_error.any_str.max_length":
        limit = str(exc.errors()[0]["ctx"]["limit_value"])
        return JSONResponse(content={"message": "The value entered is too long. Max length is " + limit, "success": False, "code": status_code}, status_code=status_code)
    elif exc.errors()[0]["type"] == "value_error.missing":
        missing = []
        for error in exc.errors():
            try:
                missing.append(error["loc"][1])
            except:
                missing.append(error["loc"][0])

        return JSONResponse(content={"message": "One or more fields are missing: " + str(missing), "succes": False, "code": status_code}, status_code=status_code)
    else:
        return JSONResponse(content={"message": exc.errors()[0]["msg"], "success": False, "code": status_code}, status_code=status_code)

@app.get("/")
async def root():
    return "Welcome to Eurostreaming Unofficial API! By @Matt0550 on GitHub"

@app.get("/status")
def api_status(request: Request):
    # Get the API uptime without microseconds
    uptime = datetime.datetime.now() - UP_START_TIME
    uptime = str(uptime).split(".")[0]

    url = request.url
    url = url.scheme + "://" + url.netloc

    return {"api": {"status": "online", "uptime": uptime, "url": url}, "eurostreaming": {"online": eurostreamingWorker.checkStatus()}}

@app.get("/shows/{page}")
async def get_shows(response: Response, page: int, response_model=ShowsResponse):
    # Get the shows from the Eurostreaming website
    shows = eurostreamingWorker.getShows(page)
    
    if shows.shows:
        # Return a list of Show objects
        return ShowsResponse(shows=shows.shows, maxPages=shows.maxPages)
    else:
        # Return an empty list
        response.status_code = 404
        return ShowsResponse([], 0, False)
    
@app.get("/search")
async def search_shows(response: Response, q: str, page: int = 0, response_model=ShowsResponse):
    print(q)
    
    # Search for shows from the Eurostreaming website
    shows = eurostreamingWorker.searchShows(query=q, page=page)
    
    if shows.shows:
        # Return a list of Show objects
        return ShowsResponse(shows=shows.shows, maxPages=shows.maxPages)
    else:
        # Return an empty list
        response.status_code = 404
        return ShowsResponse(shows=[], maxPages=0)
    
@app.get("/show")
async def get_show(response: Response, path: str, alsoEpisodes: bool = True, response_model=Show):
    # Parse path add first / if not present
    if path[0] != "/":
        path = "/" + path
        
    # Get the show from the Eurostreaming website
    show = eurostreamingWorker.getShow(path, alsoEpisodes)
    
    if show:
        # Return a Show object
        return show
    else:
        # Return an empty Show object
        response.status_code = 404
        return Show(title="", url="", image="")