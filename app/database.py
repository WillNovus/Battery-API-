from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
#import psycopg2
#import time

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#while True:   
    #try:
        #conn = psycopg2.connect(host = 'localhost', dbname = 'fastapi', user = 'postgres', password = '18061999')
        #print("Database connection was successful!")
        #break
    #except Exception as error:
        #print("Connecting to Database failed")
        ##time.sleep(2)
