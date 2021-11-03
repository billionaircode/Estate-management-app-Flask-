import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_moment import Moment

from security import authenticate, identity
from resources.user import UserRegister, UserList, User, GuardList
from resources.staff import Staff, StaffList
from resources.guest import Guest, GuestList

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Guest, '/guest/<string:name>')
api.add_resource(GuestList, '/guests')
api.add_resource(Staff, '/staff/<string:name>')
api.add_resource(StaffList, '/staffs')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<string:username>')
api.add_resource(GuardList, '/guards')

moment = Moment(app)

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
