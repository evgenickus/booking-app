from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

try:
  DATABASE_URL = os.getenv("DATABASE_URL")
  engine = create_engine(DATABASE_URL, echo=True)
except:
  print("db service not found")
  engine = create_engine("sqlite+pysqlite:///./booking.db", echo=True)

if not database_exists(engine.url):
  create_database(engine.url)

metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
  metadata=metadata