from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_rooms():
  """
  Тестирует созданы ли комнаты в базе
  """
  response = client.get("/rooms")
  assert response.status_code == 200
  assert len(response.json()) == 2

def test_create_user():
  """
  Тестирует endpoint для создания пользователя в базе
  """
  response = client.post("/users/add", json={
    "login": "Test_User",
    "password": "password",
    "admin": True
    }
  )
  assert response.status_code == 200
  assert response.json() == {
    "login": "Test_User",
    "admin": True
    }
