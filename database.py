from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://software_db_77lj_user:adpbCPTelkHEmZO95EIl9e7w6jbDRcLj@dpg-dbdmnvtg1s2s73c1gfk0-a.oregon-postgres.render.com/software_db_77lj"
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
Base = declarative_base() 

def get_db(): 
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close() 
