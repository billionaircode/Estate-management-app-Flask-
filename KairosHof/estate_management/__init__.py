import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import stripe



stripe_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
#app.config['UPLOAD_EXTENSIONS'] = ['.jpeg', '.jpg', '.png']
#app.config['UPLOAD_FOLDER'] = '/static/profile_pics'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'core.login'



from estate_management.core.userviews import core

app.register_blueprint(core)
