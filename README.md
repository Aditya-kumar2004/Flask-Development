# Employee Management System (EMS)

A comprehensive Flask-based web application designed to manage employee profiles. This application provides full CRUD operations, advanced data searching, dynamic multi-column sorting, and range-based filtering, all integrated with state-preserving pagination.

## 📊 Preview

![Dashboard Preview](employee_management_dashboard.png)

---

## 🚀 Key Features

* **Full CRUD Operations:** Add new employees, view comprehensive details, update existing records, and delete profiles.
* **State-Preserving Pagination:** Limits listings to 5 records per page, showing the current page progress and total records.
* **Multi-Column Search:** Search for records matching name, email, or department.
* **Dynamic Sorting:** Click on headers (ID, Name, Department, Salary, Email) to toggle sorting in Ascending or Descending order.
* **Advanced Filtering:** Filter listings by department and specify minimum or maximum salary ranges.
* **Combined State Retention:** All filters, search keywords, and sorting columns persist across page numbers.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database & ORM:** MySQL Community Server, Flask-SQLAlchemy (ORM)
* **Migrations:** Flask-Migrate (Alembic)
* **Frontend:** HTML5, CSS3, Jinja2 Templates, Bootstrap 5

---

## 💻 Installation and Setup Instructions

Follow these steps to run the application locally on your machine:

### 1. Set Up the Virtual Environment
Activate your terminal inside the project directory and create a virtual environment:
```bash
# Create virtual environment
python -m venv myvenv

# Activate virtual environment (Windows)
myvenv\Scripts\activate
```

### 2. Install Dependencies
Install all the required python packages:
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
Open config.py and update the database URI with your MySQL username, password, and database name:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost:3306/database_name"
```

### 4. Apply Database Migrations
Initialize the database and apply the schema migrations:
```bash
# Set Flask Application entry point
set FLASK_APP=app.py

# Initialize migrations folder
flask db init

# Generate migration scripts
flask db migrate -m "Initial setup"

# Apply changes to your MySQL database
flask db upgrade
```

### 5. Seed Database (Optional)
Run the seeding script to populate your database with 20 realistic employees for testing search, pagination, and sorting:
```bash
python seed.py
```

### 6. Run the Application
Start the Flask development server:
```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000/` (which will redirect you to the home dashboard `/home`).
