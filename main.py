from fastapi import FastAPI
from fastapi import HTTPException, Path
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(
    title="Library"
)


class Book(BaseModel):
    book_id: int = Field(gt=0)
    name: str = Field(max_length=113)
    year_published: int = Field(gt=0)


books = [
    Book(book_id=1, name="War and Peace", year_published=1873),
    Book(book_id=2, name="Sapiens", year_published=2011),
    Book(book_id=3, name="Pride and prejudice", year_published=1813),
]


@app.get("/books/", response_model=List[Book])
async def read_library():
    if books:
        return books
    raise HTTPException(status_code=500, detail="no database")


@app.get("/book/{book_id}", status_code=200, response_model=Book)
async def read_book(book_id: int):
    if books:
        for book in books:
            if book.book_id == book_id:
                return book
    raise HTTPException(status_code=404, detail="no book with this id")


def book_exists(new_book):
    return any(book.book_id == new_book.book_id for book in books)


@app.post("/book/", status_code=201)
async def create_book(new_book: Book):
    if not books:
        raise HTTPException(status_code=500, detail="database is down")
    if book_exists(new_book):
        raise HTTPException(status_code=404,
                            detail="book with this id already exists")
    books.append(new_book)


def find_id(books: List, book_id: int) -> List:
    return [i for i, book in enumerate(books) if book.book_id == book_id]


@app.put("/book/{book_id}", status_code=200)
async def update_book(new_book: Book, book_id: int = Path(...)):
    if books:
        found = find_id(books, book_id)
        i = found[0]
        if len(found) == 0:
            raise HTTPException(status_code=404,
                                detail="no such book for update")
        if books[i] == new_book:
            raise HTTPException(status_code=304,
                                detail="no data to change")
        books[i] = new_book
        return
    raise HTTPException(status_code=404, detail="no such book")


@app.delete("/book/{book_id}", status_code=204)
async def delete_book(book_id: int = Path(...)):
    if not books:
        raise HTTPException(status_code=500, detail="database is down")
    found = find_id(books, book_id)
    if len(found) == 0:
        raise HTTPException(status_code=404, detail="no such book for remove")
    del books[found[0]]
    return


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
