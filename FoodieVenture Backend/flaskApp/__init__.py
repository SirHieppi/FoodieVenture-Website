from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = '123456'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///@localhost/flaskalchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/flaskalchemy'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) #max 20 characters
    choices = db.Column(db.String(500), default='{"choices": []}') # stored as json
    canGenerateResults = db.Column(db.String(5), default="false")

    def __repr__(self):
        return f"User('{self.username}')"

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    breakfast = db.Column(db.JSON, default="")
    lunch = db.Column(db.JSON, default="")
    dinner = db.Column(db.JSON, default="")
    dessert = db.Column(db.JSON, default="")
    coffee = db.Column(db.JSON, default="")
    milkTea = db.Column(db.JSON, default="")

from flaskApp import routes