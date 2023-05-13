from fastapi.testclient import TestClient
from fastapi import status
import json
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
    # mock_response = Mock()
    # mock_response.json.return_value = {"id": 1,
    #                                    "name": "Idiot",
    #                                    "year_published": 1868}
    # monkeypatch.setattr(requests, 'get', lambda url: mock_response)
    response = client.get('/books')
    assert response.status_code == status.HTTP_200_OK
    # assert response.json() == [{"id": 1,
    #                             "name": "Idiot",
    #                             "year_published": 1868}]

