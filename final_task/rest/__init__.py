from flask_restful import Api

from .department_api import DepartmentList
from .employee_api import EmployeeList


def create_api(app):
    api = Api(app)
    api.add_resource(department_api.DepartmentList, '/api/departments_list')
    api.add_resource(department_api.Department, '/api/departments/<id>')
    api.add_resource(employee_api.EmployeeList, '/api/employees_list')
    api.add_resource(employee_api.Employee, '/api/employees/<id>')
    return api
