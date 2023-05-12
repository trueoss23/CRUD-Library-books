from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Library"
)


class Book(BaseModel):
    book_id: int
    name: str
    year_published: int


books = [
    Book(book_id=1, name="War and Peace", year_published=1873),
    Book(book_id=2, name="Sapiens", year_published=2011),
    Book(book_id=3, name="Pride and prejudice", year_published=1813),
]


@app.get("/library")
async def read_library():
    if books:
        return books
    raise HTTPException(status_code=500, detail="no database")


@app.get("/library/{book_id}", status_code=200)
async def read_book(book_id: int):
    if books:
        for book in books:
            if book.book_id == book_id:
                return book
    raise HTTPException(status_code=404, detail="no book with this id")


@app.post("/library", status_code=201)
async def create_book(book: Book):
    if books:
        books.append(book)
    raise HTTPException(status_code=500, detail="no database")


@app.put("/library", status_code=200)
async def update_book(book: Book, new_book: Book):
    if books:
        if book in books:
            i = books.index(book)
            if books[i] == new_book:
                raise HTTPException(status_code=304,
                                    detail="no data to change")
            books[i] = new_book
    raise HTTPException(status_code=404, detail="no such book")


@app.delete("/library", status_code=204)
async def delete_book(book: Book):
    if books:
        if book in books:
            books.remove(book)
        raise HTTPException(status_code=404, detail="no such book for remove")
    raise HTTPException(status_code=500, detail="no database")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
