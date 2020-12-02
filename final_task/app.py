from flask import render_template, request, redirect, jsonify, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_restful import Api, Resource, abort, reqparse
import json
from final_task import create_app

app = create_app()
api = Api(app)
db = SQLAlchemy(app)


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)


class DepartmentModel(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class EmployeeModel(db.Model):
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
            department = DepartmentModel(name)
            db.session.add(department)
            db.session.commit()
            return redirect('/')
        except:
            return Exception
    else:
        return render_template("add_department.html")


@app.route("/<int:id>/delete_department")
def delete_department(id):
    department = DepartmentModel.query.get_or_404(id)
    employees = EmployeeModel.query.all()
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
    department = DepartmentModel.query.get(id)
    if request.method == "POST":
        tmp = department.name
        new_name = request.form["name"]
        department.name = new_name
        if tmp != new_name:
            employees = EmployeeModel.query.all()
            for i in employees:
                if i.department == tmp:
                    i.department = new_name
        try:
            db.session.commit()
            return redirect('/')
        except:
            return Exception
    else:
        departments = DepartmentModel.query.get(id)
        return render_template("department.html", departments=departments)


@app.route("/add_employee", methods=["POST", "GET"])
def add_employee():
    departments = DepartmentModel.query.all()
    if request.method == "POST":
        department = request.form["department"]
        name = request.form["name"]
        b_date = request.form["b_date"]
        salary = request.form["salary"]
        try:
            employee = EmployeeModel(department, name, b_date, salary)
            db.session.add(employee)
            db.session.commit()
            return redirect('/')
        except:
            return Exception
    else:
        return render_template("add_employee.html", departments=departments)


@app.route("/<int:id>/delete_employee")
def delete_employee(id):
    employee = EmployeeModel.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect('/')
    except:
        return Exception


@app.route("/<int:id>/edit_employee", methods=["POST", "GET"])
def edit_employee(id):
    employee = EmployeeModel.query.get(id)
    departments = DepartmentModel.query.all()
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
        employees = EmployeeModel.query.get(id)
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
    employees = EmployeeModel.query.all()
    departments = DepartmentModel.query.all()
    salaries = {}
    for d in departments:
        salaries[d.id] = get_avg_salary(d.name, employees)
    return render_template("departments.html", departments=departments, salaries=salaries)


@app.route("/employees")
def employees():
    employees = EmployeeModel.query.all()
    return render_template("employees.html", employees=employees)


@app.route("/search/b_date", methods=["POST", "GET"])
def search_by_date():
    employees = EmployeeModel.query.all()
    res_by_date = []
    if request.method == "POST":
        for e in employees:
            if request.form["b_date"] == e.b_date:
                res_by_date.append(e)
        return render_template("search.html", res_by_date=res_by_date)
    return render_template("search.html")


@app.route("/search/b_period", methods=["POST", "GET"])
def search_by_period():
    employees = EmployeeModel.query.all()
    res_by_period = []
    if request.method == "POST":
        for e in employees:
            if request.form["b_date_from"] <= e.b_date <= request.form["b_date_to"]:
                res_by_period.append(e)
        return render_template("search.html", res_by_period=res_by_period)
    return render_template("search.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/")
def index():
    departments = DepartmentModel.query.all()
    employees = EmployeeModel.query.all()
    return render_template("index.html", departments=departments, employees=employees)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
