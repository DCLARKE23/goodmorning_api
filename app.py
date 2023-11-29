from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from task import task_api
from link import link_api
from weather import weather_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goodmorning.db'
db = SQLAlchemy(app)

# Blueprint Registration TODO: make sure i wouldn't be breaking anything like this
app.register_blueprint(task_api)
app.register_blueprint(link_api)
app.register_blueprint(weather_api)

# Database Tables
class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(100), nullable = False)
    time = db.Column(db.Integer, nullable = False)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(200), nullable = False)
    name = db.Column(db.String(50), nullable = False)

if __name__ == "__main__":
    app.run()