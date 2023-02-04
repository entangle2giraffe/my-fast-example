from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from .env import *

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_admin}:{db_passwd}@{db_url}/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(bind=engine)

Base = declarative_base()