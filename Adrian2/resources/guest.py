from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.guest import GuestModel
from code_gen import code_gen
from flask_login import current_user


class Guest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        )
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    '''
    parser.add_argument('visit date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    '''
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
    parser.add_argument('entry_code',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        guest = GuestModel.find_by_name(name)
        if guest:
            return guest.json()
        return {'message': 'guest not found'}, 404

    @jwt_required()
    def post(self, name):

        if GuestModel.find_by_name(name):
            return {'message': "A guest with name '{}' already exists.".format(name)}, 400

        #entry_code = code_gen()
        #parser.add_argument('Entry code')

        data = Guest.parser.parse_args()

        guest = GuestModel(data['current_user.id'], data['name'], data['gender'], data['telephone'], data['entry_code'])

        try:
            guest.save_to_db()
            guest.send_message()
        except:
            return {"message": "An error occurred registering the guest"}, 500

        return guest.json(), 201

    @jwt_required()
    def delete(self, name):
        guest = GuestModel.find_by_name(name)
        if guest:
            guest.delete_from_db()
            return {'message': 'guest deleted.'}
        return {'message': 'guest not found.'}, 404

    @jwt_required()
    def put(self, name):
        data = guest.parser.parse_args()

        guest = GuestModel.find_by_name(name)

        if guest:
            guest.telephone = data['telephone']
        else:
            guest = GuestModel(name, **data)

        guest.save_to_db()

        return guest.json()


class GuestList(Resource):
    @jwt_required()
    def get(self):
        return {'guests': list(map(lambda x: x.json(), GuestModel.query.all()))}
