from fastapi.testclient import TestClient
from fastapi import status
import json
from unittest.mock import patch
from main import app, Book

client = TestClient(app=app)
test_libary = [
    Book(book_id=1,
         name="War and Peace",
         year_published=1873),
    Book(book_id=2,
         name="Sapiens",
         year_published=2011),
    Book(book_id=3, name="Pride and prejudice",
         year_published=1813),
]


@patch("main.books", list(test_libary))
def test_get_id_correct_id():
    response = client.get('/book/2')
    assert response.status_code == status.HTTP_200_OK
    data = json.loads(response.content)
    assert data["book_id"] == 2


@patch("main.books", list(test_libary))
def test_get_id_uncorrect_id():
    response = client.get('/book/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch("main.books", list(test_libary))
def test_get_database_correct():
    response = client.get('/books')
    assert response.status_code == status.HTTP_200_OK


@patch("main.books", list(test_libary))
def test_post_add_book_correct():
    new_book = Book(book_id=4,
                    name="The Three Musketeers",
                    year_published=1844)
    response = client.post('/book', json=new_book.dict())
    assert response.status_code == status.HTTP_201_CREATED


@patch("main.books", list(test_libary))
def test_post_add_duplicate_book_id():
    new_book = Book(book_id=3,
                    name="The Three Musketeers",
                    year_published=1844)
    response = client.post('/book', json=new_book.dict())
    assert response.status_code == status.HTTP_409_CONFLICT


@patch("main.books", list(test_libary))
def test_update_book_correct_id():
    new_book = Book(book_id=4,
                    name="The Three Musketeers",
                    year_published=1844)
    response = client.put('book/1', json=new_book.dict())
    assert response.status_code == status.HTTP_200_OK


@patch("main.books", list(test_libary))
def test_update_uncorrect_id():
    new_book = Book(book_id=4,
                    name="War and Peace",
                    year_published=1873)
    response = client.put('book/10', json=new_book.dict())
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch("main.books", list(test_libary))
def test_update_duplicate_book():
    new_book = Book(book_id=1,
                    name="War and Peace",
                    year_published=1873)
    response = client.put('book/1', json=new_book.dict())
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


@patch("main.books", list(test_libary))
def test_delete_book_correct_id():
    response = client.delete('book/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT


@patch("main.books", list(test_libary))
def test_delete_book_uncorrect_id():
    response = client.delete('book/4')
    assert response.status_code == status.HTTP_404_NOT_FOUND
