# Employee Management System (Em_App)

## Overview

This project is a web application for managing employee information. It allows you to add new employees, list existing employees, and retrieve information about specific employees. The application also supports uploading a photo of the employee's ID tag and processes this photo to generate a non-unique employee ID.

## Contact

Feel free to also consider some of my other projects, including the ones implemented in C here:

[SergeBala's GitHub](https://github.com/SergeBala)

Email: balashevski@gmail.com

## Note

This project has only been superficially tested and needs further testing and refining!

I have included the Stupidly_simple_ocr_app_for_practice folder simply for easier reference during development.

## Technologies

- **Backend Framework**: FastAPI
- **Database**: SQLite
- **Asynchronous HTTP Client**: httpx
- **ORM**: SQLAlchemy
- **Dependency Management**: Poetry

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    ```

2. **Install dependencies**:
    ```bash
    poetry install
    ```

3. **Initialize the database**:
    Ensure the database tables are created by running the application once.

## Running the Application

### Service 1 (Main Application)

1. **Run Service 1**:
    ```bash
    poetry run uvicorn em_app.main:app --reload --port 8800
    ```

2. **SwaggerUI**:
    Open your browser and go to [http://localhost:8800/docs](http://localhost:8800/docs) to access the SwaggerUI interface.

### Service 2 (Photo Processing Microservice)

1. **Run Service 2**:
    ```bash
    poetry run uvicorn em_app.service2:app --reload --port 9000
    ```

## API Endpoints

### Service 1

- **Create Employee**:
    - **Endpoint**: `POST /employees/new`
    - **Description**: Add a new employee

- **List Employees**:
    - **Endpoint**: `GET /employees/list`
    - **Description**: List existing employees

- **Get Employee by ID**:
    - **Endpoint**: `GET /employees/{employee_id}`
    - **Description**: Retrieve employee information by employee ID

### Service 2

- **Process Image**:
    - **Endpoint**: `POST /process-image/`
    - **Description**: Process the uploaded photo to generate an employee ID string




