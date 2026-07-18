#this home .py will maint thee homee pagee off all html page

from flask import Blueprint, render_template, redirect, url_for
from app.models.employee import Employee
from app.models import db
from sqlalchemy import func

home_bp = Blueprint("home",__name__)

@home_bp.route("/")
def index():
    return redirect(url_for("home.home"))

#rendering html home page
@home_bp.route("/home")
def home():
    total_employees = Employee.query.count()
    
    # Calculate distinct departments
    total_departments = db.session.query(Employee.department).distinct().count()
    
    # Calculate payroll and average salary
    payroll_stats = db.session.query(
        func.sum(Employee.salary),
        func.avg(Employee.salary)
    ).first()
    
    total_payroll = payroll_stats[0] or 0
    avg_salary = payroll_stats[1] or 0
    
    # Get 5 most recently added employees
    recent_employees = Employee.query.order_by(Employee.id.desc()).limit(5).all()
    
    return render_template(
        "home.html",
        total_employees=total_employees,
        total_departments=total_departments,
        total_payroll=round(total_payroll, 2),
        avg_salary=round(avg_salary, 2),
        recent_employees=recent_employees
    )