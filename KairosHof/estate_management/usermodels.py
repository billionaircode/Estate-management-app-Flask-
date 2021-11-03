from estate_management import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Code(db.Model):
    __tablename__ = "codes"

    id = db.Column(db.Integer, primary_key=True)
    requested_for = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    gen_date = db.Column(db.DateTime, nullable=False)
    gen_code = db.Column(db.Integer)

    def __init__(self, requested_for, user_id, gen_date, gen_code):
        self.requested_for = requested_for
        self.user_id = user_id
        self.gen_date = gen_date
        self.gen_code = gen_code


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    dateofbirth = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    streetname = db.Column(db.Text, nullable=False)
    housenumber = db.Column(db.String, nullable=False)
    flatnumber = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    telephone = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String, nullable=False)


    guests = db.relationship('Guest', backref='host', lazy='dynamic')
    staffs = db.relationship('Staff', backref='boss', lazy='dynamic')
    services = db.relationship('Service', backref='requester', lazy='dynamic')
    enquiries = db.relationship('Enquiry', backref='asker', lazy='dynamic')
    news = db.relationship('Publication', backref='reporter', lazy='dynamic')
    subscriptions = db.relationship('Subscription', backref='subscriber', lazy='dynamic')

    def __init__(self, firstname, lastname, dateofbirth, username, password, streetname, housenumber, flatnumber, gender, telephone, role):
        self.firstname = firstname
        self.lastname = lastname
        self.dateofbirth = dateofbirth
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.streetname = streetname
        self.housenumber = housenumber
        self.flatnumber = flatnumber
        self.gender = gender
        self.telephone = telephone
        self.role = role

    def __repr__(self):
        return f"NAME: {self.firstname} {self.lastname}, DATE OF BIRTH: {self.dateofbirth}, GENDER: {self.gender}, PHONE NUMBER: +234{self.telephone}, ADDRESS: {self.flatnumber}, number {self.housenumber}, {self.streetname}"

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def validate_username(self, data):
        # self.username and data are the same object
        if username.data[0].isdigit():  # Check whether the first digit is a number
            raise ValidationError('Cannot start with a number')

    def validate_phone(self, data):
        '''Regular verification of mobile phone number'''
        phone = telephone.data
        if not re.search(r'^234\d{10}$', phone):
            raise ValidationError('Mobile phone number format is incorrect')


class Guest(db.Model):

    __tablename__ = 'guests'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    visit_date = db.Column(db.DateTime, default=datetime.utcnow)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    telephone = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, visit_date, firstname, lastname, gender, telephone):
        self.user_id = user_id
        self.visit_date = visit_date
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.telephone = telephone

    def __repr__(self):
        return f"Name: {self.firstname} {self.lastname}, Sex: {self.gender}, Phone Number: +234{self.telephone}, Date: {self.visit_date}, Host: {self.user_id}"


class Staff(db.Model):

    __tablename__ = 'staffs'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    dateofbirth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String, nullable=False)
    telephone = db.Column(db.Integer, nullable=False)
    jobdescription = db.Column(db.String, nullable=False)


    def __init__(self, user_id, firstname, lastname, dateofbirth, gender, telephone, jobdescription):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.dateofbirth = dateofbirth
        self.gender = gender
        self.telephone = telephone
        self.jobdescription = jobdescription

    def __repr__(self):
        return f"Name: {self.firstname} {self.lastname}, Date of birth: {self.dateofbirth}, Sex: {self.gender}, Phone Number: +234{self.telephone}, Job description: {self.jobdescription}, Boss: {self.user_id}"


class Service(db.Model):

    __tablename__ = 'services'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    service_requested = db.Column(db.String, nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, service_requested, request_date):
        self.user_id = user_id
        self.service_requested = service_requested
        self.request_date = request_date

    def __repr__(self):
        return f"{self.service_requested} requested on {self.request_date}"


class Enquiry(db.Model):

    __tablename__ = 'enquiries'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    enquiry = db.Column(db.Text, nullable=False)
    enquiry_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, enquiry, enquiry_date):
        self.user_id = user_id
        self.enquiry = enquiry
        self.enquiry_date = enquiry_date

    def __repr__(self):
        return f"Enquiry: {self.enquiry}.... Submitted on {self.enquiry_date}"


class Publication(db.Model):

    __tablename__ = 'publications'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    publication = db.Column(db.Text, nullable=False)
    news_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, reporter_id, news, news_date):
        self.user_id = user_id
        self.publication = publication
        self.news_date = news_date

    def __repr__(self):
        return f"{self.publication}.... Written on {self.news_date}"


class Subscription(db.Model):

    __tablename__ = 'subscriptions'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subscription = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    subscription_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, subscription, amount, subscription_date):
        self.user_id = user_id
        self.subscription = subscription
        self.amount = amount
        self.subscription_date = subscription_date

    def __repr__(self):
        return f"{self.amount} naira {self.subscription} was purchased on {self.news_date}"
