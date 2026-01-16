from sqlalchemy import Column, Integer, String, Date
from datetime import date
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    department = Column(String(50))
    role = Column(String(50))
    date_joined = Column(Date, default=date.today, nullable=False)
