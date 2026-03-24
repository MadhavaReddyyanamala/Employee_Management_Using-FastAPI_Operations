import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Employee Management System", page_icon="👨‍💼", layout="wide")

API_URL = st.secrets.get("API_URL", "http://127.0.0.1:8000")


def safe_request(method, endpoint, **kwargs):
    try:
        response = requests.request(method, f"{API_URL}{endpoint}", timeout=15, **kwargs)
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"API connection failed: {e}")
        return None


st.title("👨‍💼 Employee Management System")
st.caption("Streamlit frontend connected to FastAPI backend")

menu = st.sidebar.selectbox(
    "Select an option",
    ["View Employees", "Add Employee", "Search Employee", "Update Employee", "Delete Employee"]
)

if menu == "View Employees":
    st.subheader("All Employees")

    response = safe_request("GET", "/employees")
    if response and response.status_code == 200:
        employees = response.json().get("employees", [])
        if employees:
            df = pd.DataFrame(employees)
            st.dataframe(df, use_container_width=True)
            st.success(f"Total Employees: {len(employees)}")
        else:
            st.info("No employees found.")
    elif response:
        st.error("Failed to fetch employees.")


elif menu == "Add Employee":
    st.subheader("Add Employee")

    with st.form("add_employee_form"):
        emp_id = st.number_input("Employee ID", min_value=1, step=1)
        name = st.text_input("Name")
        email = st.text_input("Email")
        department = st.text_input("Department")
        role = st.text_input("Role")
        salary = st.number_input("Salary", min_value=0.0, step=100.0)

        submitted = st.form_submit_button("Add Employee")

        if submitted:
            payload = {
                "id": int(emp_id),
                "name": name.strip(),
                "email": email.strip(),
                "department": department.strip(),
                "role": role.strip(),
                "salary": float(salary),
            }

            response = safe_request("POST", "/employees", json=payload)

            if response and response.status_code == 200:
                st.success("Employee added successfully.")
            elif response:
                try:
                    st.error(response.json().get("detail", "Failed to add employee."))
                except Exception:
                    st.error("Failed to add employee.")


elif menu == "Search Employee":
    st.subheader("Search Employee by ID")

    emp_id = st.number_input("Enter Employee ID", min_value=1, step=1, key="search_id")

    if st.button("Search"):
        response = safe_request("GET", f"/employees/{int(emp_id)}")

        if response and response.status_code == 200:
            employee = response.json()
            st.json(employee)
        elif response:
            try:
                st.error(response.json().get("detail", "Employee not found."))
            except Exception:
                st.error("Employee not found.")


elif menu == "Update Employee":
    st.subheader("Update Employee")

    emp_id = st.number_input("Employee ID to Update", min_value=1, step=1, key="update_id")

    if st.button("Load Employee"):
        response = safe_request("GET", f"/employees/{int(emp_id)}")
        if response and response.status_code == 200:
            st.session_state["employee_data"] = response.json()
        elif response:
            try:
                st.error(response.json().get("detail", "Employee not found."))
            except Exception:
                st.error("Employee not found.")

    employee_data = st.session_state.get("employee_data")

    if employee_data and employee_data["id"] == int(emp_id):
        with st.form("update_employee_form"):
            name = st.text_input("Name", value=employee_data["name"])
            email = st.text_input("Email", value=employee_data["email"])
            department = st.text_input("Department", value=employee_data["department"])
            role = st.text_input("Role", value=employee_data["role"])
            salary = st.number_input("Salary", min_value=0.0, value=float(employee_data["salary"]), step=100.0)

            updated = st.form_submit_button("Update Employee")

            if updated:
                payload = {
                    "id": int(emp_id),
                    "name": name.strip(),
                    "email": email.strip(),
                    "department": department.strip(),
                    "role": role.strip(),
                    "salary": float(salary),
                }

                response = safe_request("PUT", f"/employees/{int(emp_id)}", json=payload)

                if response and response.status_code == 200:
                    st.success("Employee updated successfully.")
                    st.session_state["employee_data"] = payload
                elif response:
                    try:
                        st.error(response.json().get("detail", "Failed to update employee."))
                    except Exception:
                        st.error("Failed to update employee.")


elif menu == "Delete Employee":
    st.subheader("Delete Employee")

    emp_id = st.number_input("Employee ID to Delete", min_value=1, step=1, key="delete_id")

    if st.button("Delete Employee"):
        response = safe_request("DELETE", f"/employees/{int(emp_id)}")

        if response and response.status_code == 200:
            st.success("Employee deleted successfully.")
            if "employee_data" in st.session_state:
                del st.session_state["employee_data"]
        elif response:
            try:
                st.error(response.json().get("detail", "Failed to delete employee."))
            except Exception:
                st.error("Failed to delete employee.")