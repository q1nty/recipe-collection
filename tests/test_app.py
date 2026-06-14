import sys
import os

# добавляем корень проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_add_page():
    client = app.test_client()
    response = client.get("/add")
    assert response.status_code == 200
