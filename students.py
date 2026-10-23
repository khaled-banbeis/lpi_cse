from sqlalchemy import Column, Integer, String 
from database import Base

class Students(Base): 
    __tablename__ = "student" 
    __table_args__= {"schema":"training"}


    student_id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    name = Column(String(100), index=True) 
    email = Column(String(100), unique=True, index=True) 
    department = Column(String(100), unique=True, index=True) 
    age = Column(Integer)  