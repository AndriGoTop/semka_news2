from pydantic import BaseModel
from datetime import datetime


class NewsScheme(BaseModel):
    heading: str
    article: str
    created_at: datetime = datetime.now()

class ParsingSchemas(BaseModel):
    source: str
    limit: int = 15
    minutes_delta: int = 30