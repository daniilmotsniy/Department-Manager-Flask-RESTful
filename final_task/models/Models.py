from final_task import db


class Department(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name
        }
        return data

    def from_dict(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])


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

    def to_dict(self):
        data = {
            'id': self.id,
            'department': self.department,
            'name': self.name,
            'b_date': self.b_date,
            'salary': self.salary,
        }
        return data

    def from_dict(self, data):
        for field in ["id", "department", "name", "b_date", "salary"]:
            if field in data:
                setattr(self, field, data[field])
