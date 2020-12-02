from final_task import db


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
