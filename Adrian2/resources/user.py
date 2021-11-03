from flask_restful import Resource, reqparse, inputs
from flask_jwt import jwt_required
from models.user import UserModel
from datetime import datetime, date
#import dateutil.parser
#from models.user import json_serial


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('dateofbirth',
                        type=inputs.date,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('housenumber',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('streetname',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('gender',
                        type=str,
                        choices=['male','female'],
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('telephone',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('role',
                        type=str,
                        choices=['occupant','guard'],
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        #GET POSTED DATA
        data = UserRegister.parser.parse_args()

        #VERIFY IF USER ALREADY EXISTS OR NOT
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        #ADD POSTED DATA TO DATABASE
        user = UserModel(data['username'], data['password'], data['firstname'], data['lastname'],
                         data['dateofbirth'], data['housenumber'], data['streetname'],
                         data['gender'], data['telephone'], data['role'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201



class UserList(Resource):
    def get(self):
        return {'Users': list(map(lambda x: x.json(), UserModel.find_by_role(role="occupant")))}


class GuardList(Resource):
    def get(self):
        return {'Guards': list(map(lambda x: x.json(), UserModel.find_by_role(role="guard")))}


class User(Resource):

    #@jwt_required
    def get(self, username):
        user = UserModel.find_by_username(username).first()
        if user:
            return user.json()

        return {'message': f"{username} not found"}, 404

    #@jwt_required()
    def put(self, username):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(username)

        if user:
            user.telephone = data['telephone']
        else:
            user = UserModel(name, **data)

        user.save_to_db()

        return user.json()

    #@jwt_required()
    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404
