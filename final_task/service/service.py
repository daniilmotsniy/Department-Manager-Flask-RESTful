from final_task import db

from ..models import Department, Employee


def get_departments():
    departments = Department.query.all()
    return [department.to_json() for department in departments]


def add_department(name):
    department = Department(name)
    db.session.add(department)
    db.session.commit()


def edit_department(id, name):
    department = Department.query.get_or_404(id)
    department.name = name
    db.session.add(department)
    db.session.commit()


def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()


def get_avg_salary(department, employees) -> str:
    sum, count = 0, 0
    for e in employees:
        if e.department == department:
            sum += e.salary
            count += 1
    if count == 0:
        return format(0, '.2f')
    return format(float(sum / count), '.2f')


def get_department_by_id(id):
    department = Department.query.get(id)
    return department.to_json() if department is not None else None


def get_employees():
    employees = Employee.query.all()
    return [employee.to_json() for employee in employees]


def add_employee(name, department, salary, b_date):
    employee = Employee(name=name, department=department,
                        salary=salary, b_date=b_date)
    db.session.add(employee)
    db.session.commit()


def edit_employee(id, name, department, salary, b_date):
    employee = Employee.query.get_or_404(id)
    employee.name = name
    employee.department = department
    employee.salary = salary
    employee.b_date = b_date
    db.session.add(employee)
    db.session.commit()


def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()


# def get_employees_born_on(date):
#     date = datetime.strptime(date, '\'%m/%d/%Y\'').date()
#     employees = Employee.query.filter_by(date_of_birth=date)
#     return [employee.json() for employee in employees]


# def get_employees_born_between(start_date, end_date):
#     employees = Employee.query.filter(Employee.date_of_birth.between(start_date, end_date))
#     return [employee.json() for employee in employees]


def get_employee_by_id(id):
    employee = Employee.query.get(id)
    return employee.to_json() if employee is not None else None