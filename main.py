from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List

app = FastAPI(title="Employee Management API")

# Replace this with your actual Streamlit app URL after deployment
origins = [
    "https://your-streamlit-app-name.streamlit.app",
    "http://localhost:8501",  # for local Streamlit testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Employee(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    email: EmailStr
    department: str
    role: str
    salary: float = Field(..., ge=0)


employees: List[dict] = []


@app.get("/")
def home():
    return {"message": "Employee Management API is running"}


@app.get("/employees")
def get_employees():
    return {"employees": employees}


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for emp in employees:
        if emp["id"] == employee_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees")
def create_employee(employee: Employee):
    for emp in employees:
        if emp["id"] == employee.id:
            raise HTTPException(status_code=400, detail="Employee ID already exists")
        if emp["email"] == employee.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    employees.append(employee.model_dump())
    return {"message": "Employee added successfully", "employee": employee}


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, updated_employee: Employee):
    for index, emp in enumerate(employees):
        if emp["id"] == employee_id:
            # prevent email duplication with another employee
            for other in employees:
                if other["id"] != employee_id and other["email"] == updated_employee.email:
                    raise HTTPException(status_code=400, detail="Email already exists")

            employees[index] = updated_employee.model_dump()
            return {
                "message": "Employee updated successfully",
                "employee": updated_employee,
            }

    raise HTTPException(status_code=404, detail="Employee not found")


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for index, emp in enumerate(employees):
        if emp["id"] == employee_id:
            deleted_employee = employees.pop(index)
            return {
                "message": "Employee deleted successfully",
                "employee": deleted_employee,
            }

    raise HTTPException(status_code=404, detail="Employee not found")