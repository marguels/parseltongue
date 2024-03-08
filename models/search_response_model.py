from pydantic import BaseModel

class SearchResponseModel(BaseModel):
    content: str
    source: str