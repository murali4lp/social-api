from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg
# from psycopg.rows import dict_row

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

# Connecting using psycopg adapter - raw sql queries
# try:
#     conn = psycopg.connect(
#         host='localhost',
#         port=5432, 
#         dbname='social-api', 
#         user='postgres', 
#         password='admin',
#         connect_timeout=10, 
#         row_factory=dict_row)
#     cursor = conn.cursor()
#     print('Database connection was successful!')
# except Exception as error:
#     conn.close()
#     print('Connection to the database failed')
#     print('Error: ', error)