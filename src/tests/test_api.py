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

