from datetime import date
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


# -----------------------------
# Base schema (shared fields)
# -----------------------------
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    department: Optional[str] = Field(default=None, max_length=50)
    role: Optional[str] = Field(default=None, max_length=50)


# -----------------------------
# Create Employee (POST)
# -----------------------------
class EmployeeCreate(EmployeeBase):
    pass


# -----------------------------
# Update Employee (PUT)
# -----------------------------
class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(default=None, max_length=50)
    role: Optional[str] = Field(default=None, max_length=50)


# -----------------------------
# Response schema (GET)
# -----------------------------
class EmployeeOut(EmployeeBase):
    id: int
    date_joined: date

    class Config:
        from_attributes = True


# -----------------------------
# Pagination response
# -----------------------------
class PaginatedEmployees(BaseModel):
    items: List[EmployeeOut]
    total: int
    page: int
    page_size: int
    next_page: Optional[int]
    prev_page: Optional[int]
