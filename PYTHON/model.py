from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="templates/assets", static_url_path='/assets')
app.debug = True
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = 'data'
    id = Column(INTEGER, primary_key=True)
    air_temp = Column(REAL(), nullable=False)
    humidity = Column(REAL(), nullable=False)
    light = Column(INTEGER(), nullable=False)
    light1 = Column(INTEGER(), nullable=False)
    light2 = Column(INTEGER(), nullable=False)
    light3 = Column(INTEGER(), nullable=False)
    lock = Column(INTEGER(), nullable=False)
    coffee = Column(INTEGER(), nullable=False)

    def update(self, air_temp, humidity, light, light1, light2, light3, lock, coffee):
        self.air_temp = air_temp
        self.humidity = humidity
        self.light = light
        self.light1 = light1
        self.light2 = light2
        self.light3 = light3
        self.lock = lock
        self.coffee = coffee
        db.session.commit()
