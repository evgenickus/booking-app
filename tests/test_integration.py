import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app.dependencies import get_db
from app.database.database import Base
from app.main import app


# Адрес для тестовой базы данных
DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost/test_bd"

engine_test = create_engine(DATABASE_URL, echo=True)

# Проверка если тестовая база данных не создана, то создаем
if not database_exists(engine_test.url):
  create_database(engine_test.url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# Переопределение зависимости
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
    response = client.post("/users/", json={"login": "Evgenich", "password": "pass001", "admin": False})
    assert response.status_code == 200
    data = response.json()
    assert data["login"] == "Evgenich"
    assert data["admin"] is False
    # assert "user_id" in data

# def test_list_tasks(client):
#     # Сначала создадим задачу
#     client.post("/tasks/", json={"title": "Сделать тесты"})
#     response = client.get("/tasks/")
#     assert response.status_code == 200
#     tasks = response.json()
#     assert len(tasks) == 1
#     assert tasks[0]["title"] == "Сделать тесты"