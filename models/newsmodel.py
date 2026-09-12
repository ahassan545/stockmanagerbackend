from pydantic import BaseModel


class News(BaseModel):
    summary: str
