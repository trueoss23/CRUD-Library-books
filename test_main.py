from fastapi.testclient import TestClient
from fastapi import status
import json
from unittest.mock import patch
# import requests
from main import app
# from unittest.mock import Mock

client = TestClient(app=app)
# client = TestClient(app)


def test_get_id_correct():
    response = client.get('/book/2')
    assert response.status_code == status.HTTP_200_OK
    data = json.loads(response.content)
    assert data["book_id"] == 2


def test_get_id_uncorrect_id():
    response = client.get('/book/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_database_correct():
    response = client.get('/books')
    assert response.status_code == status.HTTP_200_OK


@patch("main.books", [])
def test_get_database_uncorrect():
    response = client.get('/books')
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
