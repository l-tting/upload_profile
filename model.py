from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6979@localhost/brian'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer,primary_key=True,nullable= False)
    file = db.Column(db.String,nullable= False)

    def __init__(self, file):
        self.file = file


with app.app_context():
    db.create_all()
