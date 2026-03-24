Employee Management System (FastAPI + Streamlit):
This project is a full-stack Employee Management System developed using FastAPI for the backend and Streamlit for the frontend. It is designed to demonstrate real-world CRUD (Create, Read, Update, Delete) operations along with API integration and cloud deployment. The application allows users to manage employee data efficiently through a simple and interactive dashboard interface.

The backend of the application is built using FastAPI, where RESTful APIs are created to handle all employee operations such as adding new employees, retrieving employee records, updating details, and deleting entries. These APIs are tested using FastAPI’s built-in Swagger UI. The frontend is developed using Streamlit, which provides a clean and responsive user interface that communicates with the backend through HTTP requests.

The application includes features such as adding employees, viewing all employee records, searching employees by ID, updating employee details, and deleting records. It also includes a dashboard that displays key metrics like total number of employees, average salary, and department distribution. Additionally, the system automatically generates employee IDs to ensure uniqueness and improve usability.

For deployment, the FastAPI backend is hosted on Render, while the Streamlit frontend is deployed on Streamlit Community Cloud. This separation of frontend and backend demonstrates a real-world architecture where services communicate over APIs.

🔗 Live Application:
Frontend: https://employeemanagementusing-fastapioperations-huo9tsw46mcxmebcaqsa.streamlit.app/

Backend API Docs: https://employee-management-using-fastapi.onrender.com/

Currently, the project uses in-memory storage, which means the data is not persistent and may reset when the server restarts. This design choice was made to keep the implementation simple and focused on API and frontend integration.

In the future, this project can be enhanced by integrating a database such as PostgreSQL, adding authentication and authorization, enabling file uploads, and implementing advanced analytics features.

👨‍💻 Author
Yanamala Madhava Reddy
