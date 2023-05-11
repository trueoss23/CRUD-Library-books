from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI(
    title="Library"
)

books = [
    {"name": "War and Peace", "year_published": 1873, },
    {"name": "Sapiens", "year_published": 2011, },
    {"name": "Pride and prejudice", "year_published": 1813, },
]


@app.get("/library/get_library")
async def read_library():
    return books


@app.get("/libary/{book_name}")
async def read_book(book_name: str):
    res = []
    if books:
        for book in books:
            if book["name"] == book_name:
                res.append(book)
    return res


@app.post("/libary/create")
async def create_book(book: dict):
    if books:
        if book not in books:
            if list(book.keys()) == list(books[0].keys()):
                books.append(book)
                return f"Added {book}"
            else:
                raise HTTPException(status_code=400, detail="incorrect book")
        else:
            return "book is already in library"
    else:
        books.append(book)
        # this weakness if we clean library and will add bad book
        return f"Added {book}"


@app.put("/libary/update")
async def update_book(book: dict, new_book: dict):
    if books:
        if book in books:
            i = books.index(book)
            books[i] = new_book
            return "OK"
    return "Book is not found"


@app.delete("/libary/delete")
async def delete_book(book: dict):
    if books:
        if book in books:
            books.remove(book)
            return f"delete {book}"
        return f"Not found {book}"
    else:
        return "library is empty"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
