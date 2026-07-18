from flask import Blueprint,request,redirect,url_for,render_template,flash,session

from app.models.employee import Employee
from app.models import db 

employee_bp = Blueprint("employee",__name__)
employee_addlist = []   #added becausee when wee are enetering data in form then thiss data will store in thee aray

@employee_bp.route("/employeeDepartment")
def goToDeparmentpage():
    return redirect(url_for("department.departmentHome"))



@employee_bp.route("/employee/list")
def employee_list():
    # for the page number we use thiss command's 
    page = request.args.get('page', 1, type=int)
    #added the searching functionality
    search_query = request.args.get('search', '', type=str)
    #added the sorting functionality
    sort_by = request.args.get('sort', 'id', type=str)
    direction = request.args.get('direction', 'asc', type=str)

    # added the filtering functionality
    dept_filter = request.args.get('department', '', type=str)
    min_salary = request.args.get('min_salary', None, type=float)
    max_salary = request.args.get('max_salary', None, type=float)

    per_page = 5
    #building query for the pagination
    query = Employee.query
    #If there is a search query, filter by Name, Email, or Department
    if search_query:
        query = query.filter(
            (Employee.name.like(f"%{search_query}%")) |
            (Employee.email.like(f"%{search_query}%")) |
            (Employee.department.like(f"%{search_query}%"))
        )

    # Apply department and salary range filters
    if dept_filter:
        query = query.filter(Employee.department == dept_filter)
    if min_salary is not None:
        query = query.filter(Employee.salary >= min_salary)
    if max_salary is not None:
        query = query.filter(Employee.salary <= max_salary)

    #added the sorting functionality
    sort_columns = {
        'id': Employee.id,
        'name': Employee.name,
        'email': Employee.email,
        'department': Employee.department,
        'salary': Employee.salary
    }
    #for the sorting of the employees
    sort_column = sort_columns.get(sort_by, Employee.id)

    #Add sorting to the query
    if direction == 'desc':
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column)
    
    # Get all unique departments for the filter dropdown
    distinct_depts = db.session.query(Employee.department).distinct().all()
    departments = [dept[0] for dept in distinct_depts if dept[0]]

    #applying the pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    #sending to the frontend for the display of the employees data
    return render_template(
        "employee.html",
        employees=pagination.items,
        pagination=pagination,
        departments=departments
    )


@employee_bp.route("/employee/add", methods=["POST", "GET"])
def employeeAdd():
    if session.get('user_role') != 'Admin':
        flash("Access denied! Only administrators can perform this action.", "danger")
        return redirect(url_for("employee.employee_list"))

    if request.method == "POST":

        employee = Employee(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"],
            salary=float(request.form["salary"]),
            department=request.form["department"]
        )

        # creating database query
        db.session.add(employee)
        # run the query
        db.session.commit()

        return redirect(url_for("employee.employee_list"))

    return render_template("add_employee.html")

#to see full edit the detials of emlployee
@employee_bp.route("/employee/employeeUpdate/<int:id>", methods=["GET", "POST"])
def employeeUpdate(id):
    if session.get('user_role') != 'Admin':
        flash("Access denied! Only administrators can perform this action.", "danger")
        return redirect(url_for("employee.employee_list"))

    employee = Employee.query.get_or_404(id)  

    if request.method == "POST":
        employee.name = request.form["name"]
        employee.email = request.form["email"]
        employee.department = request.form["department"]
        employee.salary = request.form["salary"]
        employee.password = request.form["password"]

        db.session.commit()
        return redirect(url_for("employee.employee_list"))

    return render_template("edit_employee.html", employee=employee)

# to see full details of employee
@employee_bp.route("/employee/employeeDetails/<int:id>")
def employeeDetails(id):
    employee = Employee.query.get_or_404(id)
    return render_template("employee_detail.html", employee=employee)

# to delete an employee
@employee_bp.route("/employee/employeeDelete/<int:id>")
def employeeDelete(id):
    if session.get('user_role') != 'Admin':
        flash("Access denied! Only administrators can perform this action.", "danger")
        return redirect(url_for("employee.employee_list"))

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()

    return redirect(url_for("employee.employee_list"))

    #contact    
@employee_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thank you for reaching out! Your message has been received.", "success")
        return redirect(url_for("employee.contact"))
    return render_template("contact.html")


#Authentication Flow
#Registration Route
@employee_bp.route("/employee/register", methods=["GET", "POST"])
def register():
    # Redirect to home if user is already logged in
    if session.get('user_id'):
        return redirect(url_for('home.home'))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        salary = float(request.form.get("salary") or 0)
        department = request.form["department"]
        role = request.form.get("role", "Employee")

        # Prevent registering with an already existing email
        exists = Employee.query.filter_by(email=email).first()
        if exists:
            flash("Email address is already registered!", "danger")
            return redirect(url_for("employee.register"))

        # Create a new Employee in the database
        new_employee = Employee(
            name=name,
            email=email,
            password=password,
            salary=salary,
            department=department,
            role=role
        )
        db.session.add(new_employee)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("employee.login"))

    return render_template("register.html")

#Login Route
@employee_bp.route("/employee/login", methods=["GET", "POST"])
def login():
    # Redirect to home if user is already logged in
    if session.get('user_id'):
        return redirect(url_for('home.home'))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Query database for matching email & password
        employee = Employee.query.filter_by(email=email, password=password).first()
        
        if not employee:
            flash("Invalid email or password!", "danger")
            return redirect(url_for("employee.login"))

        # Store logged-in user info in Flask Session
        session['user_id'] = employee.id
        session['user_name'] = employee.name
        session['user_role'] = employee.role

        flash(f"Welcome back, {employee.name}!", "success")
        return redirect(url_for("home.home"))

    return render_template("login.html")

#Logout Route
@employee_bp.route("/employee/logout")
def logout():
    # Clear the session state
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_role', None)
    flash("You have been logged out.", "info")
    return redirect(url_for("employee.login"))




#thiss all come unde the advane CRUD operation
# funtcionalitis like 
#pagination 
#sorting 
#filtering
#serching