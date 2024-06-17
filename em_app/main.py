from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from em_app.database import SessionLocal, engine, Base
from em_app import crud, models, schemas
import shutil
import os
import httpx

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employees/new", response_model=schemas.Employee)
async def create_employee(
    first_name: str,
    last_name: str,
    age: int,
    position: str,
    remote: bool,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save the photo
    photos_dir = "id_photos1"
    os.makedirs(photos_dir, exist_ok=True)
    photo_path = os.path.join(photos_dir, photo.filename)
    try:
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save photo: {str(e)}")

    # Send the photo to Service 2 to get the employee ID
    try:
        async with httpx.AsyncClient() as client:
            with open(photo_path, "rb") as file:
                response = await client.post(
                    "http://localhost:9000/process-image/",
                    files={"file": (photo.filename, file, photo.content_type)},
                )
                response.raise_for_status()
                employee_id = response.json()["employee_id"]
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error sending photo to Service 2: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error response from Service 2: {e.response.text}")

    # Create the employee entry
    employee_create = schemas.EmployeeCreate(
        first_name=first_name,
        last_name=last_name,
        age=age,
        position=position,
        remote=remote
    )
    db_employee = crud.create_employee(db=db, employee=employee_create, employee_id=employee_id)
    return db_employee

# @app.post("/employees/new", response_model=schemas.Employee)
# async def create_employee(
#     first_name: str,
#     last_name: str,
#     age: int,
#     position: str,
#     remote: bool,
#     photo: UploadFile=File(...),
#     db: Session = Depends(get_db)
# ):
#     # Simulate interaction with Service 2
#     employee_id = "123"  # Mock response from Service 2

#     # Save the photo
#     photos_dir = "id_photos1"
#     os.makedirs(photos_dir, exist_ok=True)
#     photo_path = os.path.join(photos_dir, photo.filename)
#     try:
#         with open(photo_path, "wb") as buffer:
#             shutil.copyfileobj(photo.file, buffer)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to save photo: {str(e)}")
#     # Create the employee entry
#     employee_create = schemas.EmployeeCreate(
#         first_name=first_name,
#         last_name=last_name,
#         age=age,
#         position=position,
#         remote=remote
#     )
#     db_employee = crud.create_employee(db=db, employee=employee_create, employee_id=employee_id)
#     return db_employee

@app.get("/employees/list", response_model=list[schemas.Employee])
async def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

@app.get("/employees/{employee_id}", response_model=schemas.Employee)
async def read_employee(employee_id: str, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Employee Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)








# from fastapi import FastAPI, Depends, HTTPException, UploadFile
# from sqlalchemy.orm import Session
# from em_app.database import SessionLocal, engine, Base
# from em_app import crud, models, schemas
# import shutil



# # Create the database tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/employees/new", response_model=schemas.Employee)
# async def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
#     # Simulate interaction with Service 2
#     employee_id = "123"  # Mock response from Service 2

#     # Save the photo
#     photo_path = f"photos/{employee.photo.filename}"
#     with open(photo_path, "wb") as buffer:
#         shutil.copyfileobj(employee.photo.file, buffer)

#     db_employee = crud.create_employee(db=db, employee=employee, employee_id=employee_id)
#     return db_employee

# @app.get("/employees/list", response_model=list[schemas.Employee])
# async def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     employees = crud.get_employees(db, skip=skip, limit=limit)
#     return employees

# @app.get("/employees/{employee_id}", response_model=schemas.Employee)
# async def read_employee(employee_id: int, db: Session = Depends(get_db)):
#     db_employee = crud.get_employee(db, employee_id=employee_id)
#     if db_employee is None:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     return db_employee

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the Employee Management API"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8800)