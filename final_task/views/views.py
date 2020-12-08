from flask import render_template, request
from ..models import Department, Employee
from . import user


@user.route("/departments")
def departments():
    departments = Department.query.all()
    return render_template("departments.html", departments=departments)


@user.route("/employees")
def employees():
    employees = Employee.query.all()
    return render_template("employees.html", employees=employees)


@user.route("/search/b_date", methods=["POST", "GET"])
def search_by_date():
    employees = Employee.query.all()
    res_by_date = []
    if request.method == "POST":
        for e in employees:
            if request.form["b_date"] == e.b_date:
                res_by_date.append(e)
        return render_template("search.html", res_by_date=res_by_date)
    return render_template("search.html")


@user.route("/search/b_period", methods=["POST", "GET"])
def search_by_period():
    employees = Employee.query.all()
    res_by_period = []
    if request.method == "POST":
        for e in employees:
            if request.form["b_date_from"] <= e.b_date <= request.form["b_date_to"]:
                res_by_period.append(e)
        return render_template("search.html", res_by_period=res_by_period)
    return render_template("search.html")


@user.route("/search")
def search():
    return render_template("search.html")


@user.route("/")
def index():
    departments = Department.query.all()
    employees = Employee.query.all()
    return render_template("index.html", departments=departments, employees=employees)


@user.route("/add_department", methods=["POST", "GET"])
def add_department():
    return render_template("add_department.html")


@user.route("/departments/edit_department/<int:id>", methods=["POST", "GET"])
def edit_department(id):
    return render_template("department.html")