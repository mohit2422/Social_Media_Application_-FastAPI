from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# format of connection string for sqlalchemy
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Mohit#2206@localhost/fastapi'
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
