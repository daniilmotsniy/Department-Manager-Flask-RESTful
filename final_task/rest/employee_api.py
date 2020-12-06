from flask import abort, jsonify, request, Response
from flask_restful import reqparse, Resource

from ..service import service as service

parser = reqparse.RequestParser()

parser.add_argument('name')
parser.add_argument('department')
parser.add_argument('salary')
parser.add_argument('b_date')


def abort_if_employee_doesnt_exist(id):
    if service.get_employee_by_id(id) is None:
        abort(Response("Employee {} doesn't exist".format(id), 404))


class EmployeeList(Resource):
    @staticmethod
    def get():
        args = request.args

        # if len(args) == 2:
        #     return jsonify(
        #         service.get_employees_born_between(start_date=args['start_date'],
        #                                                      end_date=args['end_date']))
        # if len(args) == 1:
        #     return jsonify(employees_service.get_employees_born_on(date=args['date']))

        return jsonify(service.get_employees())

    @staticmethod
    def post():
        args = parser.parse_args()
        service.add_employee(args['name'], args['department'], args['salary'], args['b_date'])
        return "Employee added", 201


class Employee(Resource):
    @staticmethod
    def get(id):
        abort_if_employee_doesnt_exist(id)
        return jsonify(service.get_employee_by_id(id))

    @staticmethod
    def put(id_):
        args = parser.parse_args()
        employee = service.get_employee_by_id(id_)
        service.edit_employee(id_, args.get('name', employee['name']),
                                          args.get('department', employee['department']),
                                          args.get('salary', employee['salary']),
                                          args.get('b_date', employee['b_date']))
        return "Employee updated", 200

    @staticmethod
    def delete(id):
        abort_if_employee_doesnt_exist(id)
        service.delete_employee(id)
        return 'Employee deleted', 200
