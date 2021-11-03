from db import db
from datetime import datetime
from code_gen import code_gen

class GuestModel(db.Model):

    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #visit_date = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    telephone = db.Column(db.Integer)
    entry_code = db.Column(db.String)

    def __init__(self, user_id, firstname, lastname, gender, telephone, entry_code):
        self.user_id = user_id
        #self.visit_date = visit_date
        self.name = name
        self.gender = gender
        self.telephone = telephone
        self.entry_code = code_gen()

    def json(self):
        return {'host': self.user_id, 'name': self.name,
                'gender': self.gender, 'telephone': self.telephone, 'entry_code': self.entry_code}



    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def send_message(cls, telephone):
        recipient = cls.query.filter_by(telephone=telephone)

        entry_code = verifyCode()

        sender = guest.find_by_user_id(user_id)

        url = "https://"

        payload = "{\r\n    \"content\": \"Your entry code is {entry_code}\",\r\n    \"from\": \"{sender}\",\r\n    \"to\": {recipient}\r\n}"
        headers = {
            'content-type': "application/json",
            'authorization': "",
            'x-rapidapi-key': "",
            'x-rapidapi-host': ""
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
