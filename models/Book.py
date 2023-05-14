from pydantic import BaseModel, Field


class Book(BaseModel):
    book_id: int = Field(gt=0)
    name: str = Field(max_length=113)
    year_published: int = Field(gt=0)
