from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/final_task"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "false"
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Department(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Employee(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(64))
    name = db.Column(db.String(64))
    b_date = db.Column(db.String(10))
    salary = db.Column(db.Integer)

    def __init__(self, department, name, b_date, salary):
        self.department = department
        self.name = name
        self.b_date = b_date
        self.salary = salary

    def get_salary(self):
        return self.salary


@app.route("/add_department", methods=["POST", "GET"])
def add_department():
    if request.method == "POST":
        name = request.form["name"]
        try:
            department = Department(name)
            db.session.add(department)
            db.session.commit()
            return redirect('/')
        except:
            return Exception
    else:
        return render_template("add_department.html")


@app.route("/<int:id>/delete_department")
def delete_department(id):
    department = Department.query.get_or_404(id)
    employees = Employee.query.all()
    try:
        for e in employees:
            if e.department == department.name:
                db.session.delete(e)
        db.session.delete(department)
        db.session.commit()
        return redirect('/')
    except:
        return Exception


@app.route("/<int:id>/edit_department", methods=["POST", "GET"])
def edit_department(id):
    department = Department.query.get(id)
    if request.method == "POST":
        tmp = department.name
        new_name = request.form["name"]
        department.name = new_name
        if tmp != new_name:
            employees = Employee.query.all()
            for i in employees:
                if i.department == tmp:
                    i.department = new_name
        try:
            db.session.commit()
            return redirect('/')
        except:
            return Exception
    else:
        departments = Department.query.get(id)
        return render_template("department.html", departments=departments)


@app.route("/add_employee", methods=["POST", "GET"])
def add_employee():
    departments = Department.query.all()
    if request.method == "POST":
        department = request.form["department"]
        name = request.form["name"]
        b_date = request.form["b_date"]
        salary = request.form["salary"]
        try:
            employee = Employee(department, name, b_date, salary)
            db.session.add(employee)
            db.session.commit()
            return redirect('/')
        except:
            return Exception
    else:
        return render_template("add_employee.html", departments=departments)


@app.route("/<int:id>/delete_employee")
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect('/')
    except:
        return Exception


@app.route("/<int:id>/edit_employee", methods=["POST", "GET"])
def edit_employee(id):
    employee = Employee.query.get(id)
    departments = Department.query.all()
    if request.method == "POST":
        employee.department = request.form["department"]
        employee.name = request.form["name"]
        employee.b_date = request.form["b_date"]
        employee.salary = request.form["salary"]
        try:
            db.session.commit()
            return redirect('/')
        except:
            return Exception
    else:
        employees = Employee.query.get(id)
        return render_template("employee.html", employees=employees, departments=departments)


def get_avg_salary(department, employees) -> str:
    sum, count = 0, 0
    for e in employees:
        if e.department == department:
            sum += e.salary
            count += 1
    if count == 0:
        return format(0, '.2f')
    return format(float(sum / count), '.2f')


@app.route("/departments")
def departments():
    employees = Employee.query.all()
    departments = Department.query.all()
    salaries = {}
    for d in departments:
        salaries[d.id] = get_avg_salary(d.name, employees)

    return render_template("departments.html", departments=departments, salaries=salaries)


@app.route("/employees")
def employees():
    employees = Employee.query.all()
    return render_template("employees.html", employees=employees)


@app.route("/search", methods=["POST", "GET"])
def search():
    employees = Employee.query.all()
    res_by_date = []
    res_by_period = []
    if request.method == "POST":
        for e in employees:
            if request.form["b_date"] == e.b_date:
                res_by_date.append(e)
        # for e in employees:
        #     if
        return render_template("search.html", res_by_date=res_by_date, res_by_period=res_by_period)
    else:
        return render_template("search.html")


@app.route("/")
def index():
    departments = Department.query.all()
    employees = Employee.query.all()
    return render_template("index.html", departments=departments, employees=employees)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
