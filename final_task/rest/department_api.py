from flask import abort, jsonify, Response
from flask_restful import reqparse, Resource

from ..service import service as serv

parser = reqparse.RequestParser()
parser.add_argument('name')


def abort_if_department_doesnt_exist(id):
    if serv.get_department_by_id(id) is None:
        abort(Response("Department {} doesn't exist".format(id), 404))


class DepartmentList(Resource):
    @staticmethod
    def get():
        return jsonify(serv.get_departments())

    @staticmethod
    def post():
        args = parser.parse_args()
        serv.add_department(args['name'])
        return "Department added", 201


class Department(Resource):
    @staticmethod
    def get(id):
        abort_if_department_doesnt_exist(id)
        return jsonify(serv.get_department_by_id(id))

    @staticmethod
    def put(id):
        args = parser.parse_args()
        department = serv.get_department_by_id(id)
        serv.edit_department(id, args.get('name', department['name']))
        return "Department edited", 200

    @staticmethod
    def delete(id):
        abort_if_department_doesnt_exist(id)
        serv.delete_department(id)
        return 'Department deleted', 200