import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
PG_USERNAME = os.getenv('PG_USERNAME', 'NO_USERNAME')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'NO_PASSWORD')
PG_DATABASE = os.getenv('PG_DATABASE', 'NO_DB_NAME')
DATABASE_URL = os.environ.get('DATABASE_URL', f'postgresql://{PG_USERNAME}:{PG_PASSWORD}@localhost:5432/{PG_DATABASE}')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

