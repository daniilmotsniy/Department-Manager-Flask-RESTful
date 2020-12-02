from final_task import db


class DepartmentModel(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name