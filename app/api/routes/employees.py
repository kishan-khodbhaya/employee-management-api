from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.employee import Employee
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeOut,
    PaginatedEmployees,
)
from app.api.routes.auth import get_current_user
from app.core.security import require_admin


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    dependencies=[Depends(get_current_user)],  # JWT required for all routes
)

# -------------------------------------------------
# CREATE EMPLOYEE (ADMIN ONLY)
# POST /employees/
# -------------------------------------------------
@router.post(
    "/",
    response_model=EmployeeOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)

    # duplicate email check
    result = await db.execute(
        select(Employee).where(Employee.email == data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this email already exists",
        )

    employee = Employee(**data.model_dump())
    db.add(employee)
    await db.commit()
    await db.refresh(employee)

    return employee


# -------------------------------------------------
# LIST EMPLOYEES (ALL USERS)
# GET /employees/
# -------------------------------------------------
@router.get(
    "/",
    response_model=PaginatedEmployees,
)
async def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    department: Optional[str] = None,
    role: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    base_query = select(Employee)

    if department:
        base_query = base_query.where(Employee.department == department)
    if role:
        base_query = base_query.where(Employee.role == role)

    # total count
    count_stmt = select(func.count()).select_from(base_query.subquery())
    total = await db.scalar(count_stmt)

    offset = (page - 1) * page_size
    stmt = base_query.offset(offset).limit(page_size)

    result = await db.execute(stmt)
    items = result.scalars().all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "next_page": page + 1 if offset + page_size < total else None,
        "prev_page": page - 1 if page > 1 else None,
    }


# -------------------------------------------------
# GET SINGLE EMPLOYEE (ALL USERS)
# GET /employees/{id}
# -------------------------------------------------
@router.get(
    "/{employee_id}",
    response_model=EmployeeOut,
)
async def get_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
):
    employee = await db.get(Employee, employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return employee


# -------------------------------------------------
# UPDATE EMPLOYEE (ADMIN ONLY)
# PUT /employees/{id}
# -------------------------------------------------
@router.put(
    "/{employee_id}",
    response_model=EmployeeOut,
)
async def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)

    employee = await db.get(Employee, employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    update_data = data.model_dump(exclude_unset=True)

    # email uniqueness check
    if "email" in update_data:
        result = await db.execute(
            select(Employee)
            .where(Employee.email == update_data["email"])
            .where(Employee.id != employee_id)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee with this email already exists",
            )

    for field, value in update_data.items():
        setattr(employee, field, value)

    await db.commit()
    await db.refresh(employee)

    return employee


# -------------------------------------------------
# DELETE EMPLOYEE (ADMIN ONLY)
# DELETE /employees/{id}
# -------------------------------------------------
@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)

    employee = await db.get(Employee, employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    await db.delete(employee)
    await db.commit()

    return None
