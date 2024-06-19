from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from em_app import models, schemas

def get_employee(db: Session, employee_id: str):
    return db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Employee).offset(skip).limit(limit).all()

# def create_employee(db: Session, employee: schemas.EmployeeCreate, employee_id: str):
#     db_employee = models.Employee(
#         first_name=employee.first_name,
#         last_name=employee.last_name,
#         age=employee.age,
#         position=employee.position,
#         remote=employee.remote,
#         employee_id=employee_id
#     )
#     db.add(db_employee)
#     db.commit()
#     db.refresh(db_employee)
#     return db_employee

def create_employee(db: Session, employee: schemas.EmployeeCreate, employee_id: str):
    # Check if an employee with the given employee_id already exists
    existing_employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if existing_employee:
        return {"error": "This employee ID is already used by another employee"}

    # Create a new employee entry
    db_employee = models.Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        age=employee.age,
        position=employee.position,
        remote=employee.remote,
        employee_id=employee_id  
    )
    # Handle the highly unlikely case where a concurrent transaction manages to create a record with the same employee_id
    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError:
        db.rollback()
        return {"error": "Failed to create employee due to a database integrity error"}
    
def delete_employee(db: Session, employee_id: str):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if employee:
        db.delete(employee)
        db.commit()
        return {"message": "Employee deleted successfully"}
    return {"error": "Employee not found"}

def update_employee(db: Session, employee_id: str, updates: dict):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        return {"error": "Employee not found"}

    if "employee_id" in updates:
        return {"error": "Updating employee_id is not allowed"}
    
    for key, value in updates.items():
        setattr(employee, key, value)

    try:
        db.commit()
        db.refresh(employee)
        return employee
    except IntegrityError:
        db.rollback()
        return {"error": "Failed to update employee due to a database integrity error"}