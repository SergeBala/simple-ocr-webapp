from sqlalchemy.orm import Session
from em_app import models, schemas

def get_employee(db: Session, employee_id: str):
    return db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate, employee_id: str):
    db_employee = models.Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        age=employee.age,
        position=employee.position,
        remote=employee.remote,
        employee_id=employee_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate, employee_id: str):
    db_employee = models.Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        age=employee.age,
        position=employee.position,
        remote=employee.remote,
        employee_id=employee_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee