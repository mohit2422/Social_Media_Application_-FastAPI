from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# format of connection string for sqlalchemy
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# Engine will help in setting connection between postgres database to python application
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal is responsible for intercating with the Databases
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  #It is a base class

# Dependency
# It will create session with database for path operations and close when request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# connecting to Postgres Database with Fastapi
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Mohit#2206', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful !!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ",error)
#         time.sleep(2)