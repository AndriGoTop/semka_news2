from pydantic import BaseModel
from datetime import datetime


class NewsScheme(BaseModel):
    heading: str
    article: str
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True


class NewsSchemaUpdate(BaseModel):
    heading: str | None = None
    article: str | None = None
    created_at: datetime | None = None

class ParsingSchemas(BaseModel):
    source: str
    limit: int = 15
    minutes_delta: int = 30