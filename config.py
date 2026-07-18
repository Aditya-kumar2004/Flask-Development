# Config.py:- THis file contains URL, API, SecreatKey, Database Url

class Config:
    APP_NAME = "Employee Management System"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Adi12345@localhost:3306/employee_db"
    SECRET_KEY = "9262c973e3a9a8f493401d9dd06cc7f208a958c8709dcd70cae7a48db21a5661"
    SQLALCHEMY_TRACK_MODIFICATION = False
    UPLOAD_FOLDER = "uploads"
    ALGORITHM = ""
    API_KEY="123456789"
    DEBUG = True