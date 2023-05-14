from fastapi import APIRouter
from fastapi import HTTPException, Path
from typing import List
import logging
import logging.config
from models.Book import Book


logging.config.fileConfig('config.ini')
logger = logging.getLogger('my_logger')

book_router = APIRouter(prefix='/books')

books = [
    Book(book_id=1, name="War and Peace", year_published=1873),
    Book(book_id=2, name="Sapiens", year_published=2011),
    Book(book_id=3, name="Pride and prejudice", year_published=1813),
]


@book_router.get("/books/", status_code=200, response_model=List[Book])
async def read_library():
    logger.debug(f'size of database: {len(books)}')
    return books


@book_router.get("/book/{book_id}", status_code=200, response_model=Book)
async def read_book(book_id: int):
    for book in books:
        if book.book_id == book_id:
            return book
    logger.debug(f'id in books: {[elem.book_id for elem in books]}\
    current id: {book_id}')
    raise HTTPException(status_code=404, detail="no book with this id")


def book_exists(new_book):
    return any(book.book_id == new_book.book_id for book in books)


@book_router.post("/book/", status_code=201)
async def create_book(new_book: Book):
    if book_exists(new_book):
        raise HTTPException(status_code=409,
                            detail="book with this id already exists")
    books.append(new_book)
    logger.debug(f'size of database: {len(books)}')
    return


def find_id(books: List, book_id: int) -> List:
    return [i for i, book in enumerate(books) if book.book_id == book_id]


@book_router.put("/book/{book_id}", status_code=200)
async def update_book(new_book: Book, book_id: int = Path(...)):
    found = find_id(books, book_id)
    if len(found) == 0:
        raise HTTPException(status_code=404,
                            detail="no such book for update")
    i = found[0]
    if books[i] == new_book:
        raise HTTPException(status_code=304,
                            detail="no data to change")
    books[i] = new_book
    return


@book_router.delete("/book/{book_id}", status_code=204)
async def delete_book(book_id: int = Path(...)):
    found = find_id(books, book_id)
    if len(found) == 0:
        raise HTTPException(status_code=404, detail="no such book for remove")
    del books[found[0]]
    return
