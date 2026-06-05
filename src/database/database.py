from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# DATABASE_URL = "sqlite+pysqlite:///./sql_app.db"
DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost/booking"
engine = create_engine(DATABASE_URL, echo=True)

if not database_exists(engine.url):
  create_database(engine.url)
  print("Database created successfully!")
else:
  print("Database already exists.")

metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
  metadata=metadata
