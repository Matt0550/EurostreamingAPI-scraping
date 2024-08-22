from pydantic import BaseModel

class StreamingService(BaseModel):
    name: str
    url: str

class Episode(BaseModel):
    episodeNumber: str
    title: str
    urls: list[StreamingService] = None

class Season(BaseModel):
    season: str
    episodes: list[Episode]

class Show(BaseModel):
    title: str
    url: str = None
    image: str = None
    description: str = None
    seasons: list[Season] = None
    status: bool = False

class ShowsResponse(BaseModel):
    shows: list[Show]
    maxPages: int
    status: bool = False

