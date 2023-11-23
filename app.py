from flask import Flask, request, Response
import urllib, urllib.parse, urllib.request, urllib.response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)

def get_weather(city):
    pass

@app.route('/', methods=['GET'])
def get_cities():
    pass

@app.route('/', methods=['POST'])
def add_new():
    pass
    

if __name__ == "__main__":
    app.run()