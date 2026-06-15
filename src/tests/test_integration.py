import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app.dependencies import get_db
from app.database.database import Base
from app.main import app
import os

try:
  DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")
  engine_test = create_engine(DATABASE_URL_TEST, echo=True)
except:
  print("db not found")
  engine_test = create_engine("sqlite+pysqlite:///./test_db.db", echo=True)

if not database_exists(engine_test.url):
  create_database(engine_test.url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client():
  """
    Фикстура для клиента и инициализации базы банных
    Создаём таблицы перед тестом
    Удаляем таблицы после теста
  """
  app.dependency_overrides[get_db] = override_get_db
  Base.metadata.create_all(bind=engine_test)
  with TestClient(app) as test_client:
    yield test_client
  Base.metadata.drop_all(bind=engine_test)
  app.dependency_overrides.clear()

def test_create_user(client):
  """
    Тестирует endpoint для создания пользователя в тестовой базе
  """
  response = client.post("/users/add", json={"login": "Evgeniy", "password": "pass001", "admin": False})
  assert response.status_code == 200
  data = response.json()
  assert data["login"] == "Evgeniy"
  assert data["admin"] is False


def test_create_booking(client):
  """
    Тестирует endpoint для создания бронирования в тестовой базе
  """
  client.post("/rooms/add", json={"name": "Стандарт", "description": "Стандартная комната"})
  client.post("/rooms/add", json={"name": "Премиум", "description": "Премиум комната"})

  user_response = client.post("/users/add", json={
      "login": "testuser",
      "password": "testpass",
      "admin": False
  })
  assert user_response.status_code == 200

  login_resp = client.post("/token", data={
      "username": "testuser",
      "password": "testpass"
  })
  assert login_resp.status_code == 200
  token = login_resp.json()["access_token"]

  response = client.post(
      "/booking/add",
      json={
          "booking_date": "2026-06-30",
          "room": "Стандарт",
          "slot": "14-17"
      },
      headers={"Authorization": f"Bearer {token}"}
  )

  data = response.json()

  assert response.status_code == 200
  assert data["room"] == "Стандарт"
  assert data["booking_date"] == "2026-06-30"
  assert data["slot"] == "14-17"
