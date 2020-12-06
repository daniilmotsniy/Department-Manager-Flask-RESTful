from flask import render_template, request
from ..models import Department, Employee
from . import user


def get_avg_salary(department, employees) -> str:
    sum, count = 0, 0
    for e in employees:
        if e.department == department:
            sum += e.salary
            count += 1
    if count == 0:
        return format(0, '.2f')
    return format(float(sum / count), '.2f')


@user.route("/departments")
def departments():
    employees = Employee.query.all()
    departments = Department.query.all()
    salaries = {}
    for d in departments:
        salaries[d.id] = get_avg_salary(d.name, employees)
    return render_template("departments.html", departments=departments, salaries=salaries)


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