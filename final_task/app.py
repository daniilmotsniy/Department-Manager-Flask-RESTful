from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/final_task"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "false"
db = SQLAlchemy(app)


class Department(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name


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
    try:
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
        return render_template("edit_department.html", departments=departments)


@app.route("/add_employee", methods=["POST", "GET"])
def add_employee():
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
        return render_template("add_employee.html")


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
        return render_template("edit_employee.html", employees=employees)


@app.route("/search")
def about():
    return render_template("search.html")


@app.route("/")
def index():
    departments = Department.query.all()
    employees = Employee.query.all()
    return render_template("index.html", departments=departments, employees=employees)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

