from db import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models.staff import StaffModel
from models.guest import GuestModel


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(200))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    dateofbirth = db.Column(db.Date)
    housenumber = db.Column(db.String(5))
    streetname = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    telephone = db.Column(db.Integer)
    role = db.Column(db.String)

    guests = db.relationship('GuestModel', backref='host', lazy='dynamic')
    staffs = db.relationship('StaffModel', backref='boss', lazy='dynamic')

    def __init__(self, username, password, firstname, lastname,dateofbirth, housenumber,
                 streetname, gender, telephone, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.firstname = firstname
        self.lastname = lastname
        self.dateofbirth = dateofbirth
        self.housenumber = housenumber
        self.streetname = streetname
        self.gender = gender
        self.telephone = telephone
        self.role = role

    def json(self):
        return {'username': self.username, 'firstname': self.firstname, 'lastname': self.lastname,
                'dateofbirth': self.dateofbirth, 'house number': self.housenumber,
                'street name': self.streetname, 'gender': self.gender, 'telephone': self.telephone,
                'role': self.role}


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def check_password(self,password):
        return check_password_hash(self.password,password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_role(cls, role):
        return cls.query.filter_by(role=role).all()
