import streamlit as st
import requests
import pandas as pd

API_URL = st.secrets["API_URL"]

# API_URL = "https://employee-management-using-fastapi.onrender.com/"

st.set_page_config(
    page_title="Employee Management Dashboard",
    page_icon="🏢",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f6f8fb;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 2.8rem;
        padding-bottom: 1.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    [data-testid="stSidebar"] {
        background-color: #eef3fb;
    }

    .title-wrap {
        margin-top: 0.6rem;
        margin-bottom: 1.4rem;
    }

    .title-text {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f2937;
        line-height: 1.2;
        margin: 0;
        padding: 0;
    }

    .sub-text {
        color: #6b7280;
        font-size: 0.98rem;
        margin-top: 0.45rem;
        margin-bottom: 0;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        min-height: 140px;
    }

    .metric-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 22px;
    }

    .metric-value {
        font-size: 2.3rem;
        font-weight: 700;
        color: #111827;
    }

    .section-card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 44px;
        font-weight: 600;
        border: none;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 10px;
    }

    .sidebar-note {
        background: #dce8fb;
        padding: 14px;
        border-radius: 12px;
        color: #1f3b64;
        font-size: 15px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def safe_request(method, endpoint, **kwargs):
    try:
        response = requests.request(method, f"{API_URL}{endpoint}", timeout=15, **kwargs)
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"API connection failed: {e}")
        return None


def fetch_employees():
    response = safe_request("GET", "/employees")
    if response and response.status_code == 200:
        return response.json().get("employees", [])
    return []


st.markdown(
    """
    <div class="title-wrap">
        <div class="title-text">Employee Management Dashboard</div>
        <div class="sub-text">
            Professional employee operations panel powered by Streamlit and FastAPI
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

employees = fetch_employees()
df = pd.DataFrame(employees) if employees else pd.DataFrame()

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.image("https://img.icons8.com/fluency/96/organization.png", width=72)
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Add Employee", "Update Employee", "Delete Employee", "Search Employee"],
)

st.sidebar.markdown(
    """
    <div class="sidebar-note">
        <b>Backend:</b> FastAPI<br><br>
        <b>Frontend:</b> Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)

if menu == "Dashboard":
    total_employees = len(employees)
    avg_salary = 0
    total_departments = 0

    if not df.empty:
        avg_salary = round(df["salary"].mean(), 2)
        total_departments = df["department"].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Employees</div>
                <div class="metric-value">{total_employees}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Departments</div>
                <div class="metric-value">{total_departments}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Average Salary</div>
                <div class="metric-value">₹ {avg_salary}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Employee Directory")

        if not df.empty:
            search_term = st.text_input("Search by name or department")
            filtered_df = df.copy()

            if search_term:
                filtered_df = filtered_df[
                    filtered_df["name"].astype(str).str.contains(search_term, case=False, na=False)
                    | filtered_df["department"].astype(str).str.contains(search_term, case=False, na=False)
                ]

            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.info("No employee records available.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Department Summary")
        if not df.empty:
            dept_counts = df["department"].value_counts()
            st.bar_chart(dept_counts)
        else:
            st.info("No department data available.")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Add Employee":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Add New Employee")

    # AUTO GENERATE ID
    if employees:
        next_id = max(emp["id"] for emp in employees) + 1
    else:
        next_id = 1

    st.info(f"Employee ID will be auto-generated: {next_id}")

    with st.form("add_employee_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
        with col2:
            department = st.text_input("Department")
            role = st.text_input("Job Role")
            salary = st.number_input("Salary", min_value=0.0, step=1000.0)

        submitted = st.form_submit_button("Add Employee")

        if submitted:
            payload = {
                "id": next_id,
                "name": name.strip(),
                "email": email.strip(),
                "department": department.strip(),
                "role": role.strip(),
                "salary": float(salary),
            }

            response = safe_request("POST", "/employees", json=payload)

            if response and response.status_code == 200:
                st.success(f"Employee added successfully with ID {next_id}")
            elif response:
                try:
                    st.error(response.json().get("detail", "Failed to add employee."))
                except Exception:
                    st.error("Failed to add employee.")

    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Update Employee":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Update Employee Details")

    emp_id = st.number_input("Enter Employee ID", min_value=1, step=1, key="update_emp_id")

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
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Full Name", value=employee_data["name"])
                email = st.text_input("Email Address", value=employee_data["email"])
                department = st.text_input("Department", value=employee_data["department"])
            with col2:
                role = st.text_input("Job Role", value=employee_data["role"])
                salary = st.number_input(
                    "Salary",
                    min_value=0.0,
                    value=float(employee_data["salary"]),
                    step=1000.0,
                )

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
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Delete Employee":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Delete Employee Record")

    emp_id = st.number_input("Employee ID", min_value=1, step=1, key="delete_emp_id")

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
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Search Employee":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Search Employee")

    search_id = st.number_input("Enter Employee ID", min_value=1, step=1, key="search_emp_id")

    if st.button("Search Employee"):
        response = safe_request("GET", f"/employees/{int(search_id)}")
        if response and response.status_code == 200:
            emp = response.json()

            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Employee Name", emp["name"], disabled=True)
                st.text_input("Email", emp["email"], disabled=True)
                st.text_input("Department", emp["department"], disabled=True)
            with c2:
                st.text_input("Role", emp["role"], disabled=True)
                st.text_input("Salary", str(emp["salary"]), disabled=True)
                st.text_input("Employee ID", str(emp["id"]), disabled=True)
        elif response:
            try:
                st.error(response.json().get("detail", "Employee not found."))
            except Exception:
                st.error("Employee not found.")
    st.markdown("</div>", unsafe_allow_html=True)
