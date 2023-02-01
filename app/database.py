from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:changeme@localhost/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(bind=engine)

Base = declarative_base()