# Flask MySQL API - DevOps Practice Repo

A lightweight Python Flask REST API connected to a MySQL database, designed for practicing backend configuration, API testing, and cloud deployment.

## 📁 Repository Structure
```text
.
├── app.py              # Main application code with CRUD operations
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.x
* MySQL Database (Local or Cloud DB)

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone <your-repo-url>
cd <your-repo-name>
pip install -r requirements.txt
```

### 3. Database Setup
Execute the following SQL in your MySQL environment (e.g., MySQL Workbench):
```sql
CREATE DATABASE IF NOT EXISTS flaskapp_db;
USE flaskapp_db;

CREATE TABLE IF NOT EXISTS user (
    userid INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    useremail VARCHAR(255) NOT NULL
);
```
*Note: Ensure the database endpoint and credentials in `app.py` match your target environment.*

### 4. Running the Application
```bash
python app.py
```
The application will run and listen on `http://0.0.0.0:5000/`.

## 🧪 API Endpoints & cURL Testing

*   **Health Check:** `GET /`
    ```bash
    curl -X GET http://localhost:5000/
    ```
*   **Create User:** `POST /users`
    ```bash
    curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"username": "test_ops", "useremail": "ops@example.com"}'
    ```
*   **Get All Users:** `GET /users`
    ```bash
    curl -X GET http://localhost:5000/users
    ```
*   **Get Specific User:** `GET /users/1`
    ```bash
    curl -X GET http://localhost:5000/users/1
    ```
*   **Update User:** `PUT /users/1`
    ```bash
    curl -X PUT http://localhost:5000/users/1 -H "Content-Type: application/json" -d '{"username": "admin_updated", "useremail": "newadmin@example.com"}'
    ```
*   **Delete User:** `DELETE /users/1`
    ```bash
    curl -X DELETE http://localhost:5000/users/1
    ```

## 🛠️ Next Steps for Practice
* **CI/CD:** Add a GitHub Actions workflow (`.github/workflows/main.yml`) to automatically test the API on every push.
* **Containerization:** Write a `Dockerfile` to containerize this Flask application for easier deployment.
