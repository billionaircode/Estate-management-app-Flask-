from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.staff import StaffModel


class Staff(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('date of birth',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('gender',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('telephone',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        staff = StaffModel.find_by_name(name)
        if staff:
            return staff.json()
        return {'message': 'Staff not found'}, 404

    @jwt_required()
    def post(self, name):

        if StaffModel.find_by_name(name):
            return {'message': "A staff with name '{}' already exists.".format(name)}, 400

        data = Staff.parser.parse_args()

        staff = StaffModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred registering the staff"}, 500

        return staff.json(), 201

    @jwt_required()
    def delete(self, name):
        staff = StaffModel.find_by_name(name)
        if staff:
            staff.delete_from_db()
            return {'message': 'Staff deleted.'}
        return {'message': 'Staff not found.'}, 404

    @jwt_required()
    def put(self, name):
        data = Staff.parser.parse_args()

        staff = StaffModel.find_by_name(name)

        if staff:
            staff.telephone = data['telephone']
        else:
            staff = StaffModel(name, **data)

        staff.save_to_db()

        return staff.json()


class StaffList(Resource):
    @jwt_required()
    def get(self):
        return {'Staffs': list(map(lambda x: x.json(), StaffModel.query.all()))}
