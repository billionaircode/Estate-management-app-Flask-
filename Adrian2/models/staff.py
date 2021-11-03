from db import db
from datetime import datetime


class StaffModel(db.Model):

    __tablename__ = 'staffs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    dateofbirth = db.Column(db.DateTime)
    gender = db.Column(db.String)
    telephone = db.Column(db.Integer)
    jobdescription = db.Column(db.String)


    def __init__(self, user_id, firstname, lastname, dateofbirth, gender, telephone, jobdescription):
        self.user_id = user_id
        self.name = name
        self.dateofbirth = dateofbirth
        self.gender = gender
        self.telephone = telephone
        self.jobdescription = jobdescription

    def json(self):
        return {'boss': self.user_id,'name': self.name, 'date of birth': self.dateofbirth,
                'gender': self.gender, 'telephone': self.telephone, 'job description': self.jobdescription}


    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
