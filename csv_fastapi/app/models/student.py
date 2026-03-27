from sqlalchemy import Column, String, Integer, Float
from app.db.database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = Column(String(20), primary_key=True, index=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    major = Column(String(100), nullable=True)
    gpa = Column(Float, nullable=True)
    attendance = Column(Float, nullable=True)
    scholarship = Column(Integer, nullable=True)
    city = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True)
