from flask import render_template, request, redirect

from config import BaseConfig
from final_task import create_app
from final_task import db
from final_task.models import Department, Employee

app = create_app(BaseConfig)


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


if __name__ == "__main__":
    app.run(debug=True)
