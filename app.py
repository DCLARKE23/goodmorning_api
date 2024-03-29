from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import re, requests, json
from config import WEATHER_API_KEY
from dataclasses import dataclass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goodmorning.db'
db = SQLAlchemy(app)

# Global Variables
url_pattern = "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

# Database Tables
@dataclass
class City(db.Model):
    id: int
    name: str

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)

@dataclass
class Task(db.Model):
    id: int
    task: str
    time: int

    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(100), nullable = False)
    time = db.Column(db.Integer, nullable = False)

@dataclass
class Link(db.Model):
    id: int
    url: str
    name: str

    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(200), nullable = False)
    name = db.Column(db.String(50), nullable = False)

# Task Functions
@app.route('/tasks', methods=['GET'])   # for testing purposes, not strictly necessary
def get_tasks():
    tasks = Task.query.all()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    req_body = request.get_json(force=True)
    new_task = Task(task=req_body.get('task'), time=req_body.get('time'))
    for t in Task.query.all():
        if t.task == new_task.task:
            abort(400, "Task with that name already exists.")
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "task": new_task.task, "time": new_task.time})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    selected_task = Task.query.get_or_404(task_id, 'Cannot delete non-existent entry')
    db.session.delete(selected_task)
    db.session.commit()
    return "Task with ID:" + str(task_id) + " has been deleted."

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    req_body = request.get_json(force=True)
    rows_counted = Task.query.filter_by(id = task_id).update(req_body)
    if rows_counted == 0:
        abort(404, 'Cannot update non-existent entry.')
    db.session.commit()
    return "Task with ID:" + str(task_id) + " has been updated."

# Weather Functions
def get_weather(city):
    if city is None or '':
        abort(400, 'Invalid entry: null or empty string')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=" + WEATHER_API_KEY
    req = requests.get(url).json()
    if (req['cod'] == '404'):
        abort(404, 'City does not exist.')
    return req

def compile_weather_data(city):
        r = get_weather(city.name)
        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        return weather

@app.route('/weather', methods=['GET']) 
def get_cities():
    cities = City.query.all()
    weather_data = []
    if len(cities) != 0:
        for city in cities:
            weather = compile_weather_data(city)
            weather_data.append(weather)
        return weather_data
    return []

@app.route('/weather/<int:id>', methods=['GET'])
def get_specific_city(id):
    city = City.query.get_or_404(id)
    weather = compile_weather_data(city)
    return weather

@app.route('/weather', methods=['POST'])
def add_city():
    req_body = request.get_json(force=True)
    new_city = City(name=req_body.get('name'))
    get_weather(new_city.name)   # check if city exists
    cities = City.query.all()
    for c in cities:    # duplicate cities check
        if c.name == new_city.name:
            abort(400, 'Preexisting duplicate.')
    db.session.add(new_city)
    db.session.commit()
    return jsonify({"id": new_city.id, "name": new_city.name})

@app.route('/weather/<int:weather_id>', methods=['PUT'])
def update_city(weather_id):
    req_body = request.get_json(force=True)
    get_weather(req_body['name'])
    for city in City.query.all():
        if city.name == req_body['name']:
            abort(400, 'Preexisting duplicate.')
    rows_counted = City.query.filter_by(id = weather_id).update(req_body)
    if rows_counted == 0: 
        abort(404, 'Cannot update Location that does not exist.')
    db.session.commit()
    return "Location with ID: " + str(weather_id) + " updated."


@app.route('/weather/<int:weather_id>', methods=['DELETE'])
def del_city(weather_id):
    selected_city = City.query.get_or_404(weather_id, 'Cannot delete non-existent entry.')
    db.session.delete(selected_city)
    db.session.commit()
    return "Location with ID: " + str(weather_id) + " removed."

# Link Functions
@app.route('/links', methods=['GET'])   # for testing purposes
def get_links():
    links = Link.query.all()
    return jsonify(links)

@app.route('/links', methods = ['POST'])
def add_link():
    req_body = request.get_json(force=True)
    new_link = Link(url = req_body.get('url'), name= req_body.get('name'))
    if re.match(url_pattern, new_link.url) == None:
        abort(400, "The URL entered is invalid.")
    links = Link.query.all()
    for l in links:
        if l.url == new_link.url or l.name == new_link.name:
            abort(400, 'Link already exists with that name or url.')
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"id": new_link.id, "url": new_link.url, "name": new_link.name})

@app.route('/links/<int:link_id>', methods = ['PUT'])
def update_link(link_id):
    req_body = request.get_json(force=True)
    rows_counted = Link.query.filter_by(id = link_id).update(req_body)
    if rows_counted == 0:
        abort(400, 'Cannot update entry that does not exist')
    if re.match(url_pattern, req_body['url']) == None:
        abort(400, 'The URL you entered is invalid.')
    db.session.commit()
    return "Link with ID:" + str(link_id) + " updated"

@app.route('/links/<int:link_id>', methods = ['DELETE'])
def delete_link(link_id):
    selected_link = Link.query.get_or_404(link_id, 'Cannot delete link that does not exist.')
    db.session.delete(selected_link)
    db.session.commit()
    return "Link with ID:" + str(link_id) + " deleted."

if __name__ == "__main__":
    app.run(debug=True)