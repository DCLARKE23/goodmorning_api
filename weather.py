from flask import Blueprint, abort, request, jsonify
from app import City, db
import requests
from config import WEATHER_API_KEY

weather_api = Blueprint('weather_api', __name__)

def get_weather(city):
    if city is None or '':
        abort(400, 'Invalid entry: null or empty string')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=" + WEATHER_API_KEY
    req = requests.get(url).json()
    return req

def compile_weather_data(city): # Helper function
        r = get_weather(city.name)
        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        return weather

@weather_api.route('/weather', methods=['GET']) # Get all cities 
def get_cities():
    cities = City.query.all()
    weather_data = []
    if len(cities) != 0:
        for city in cities:
            weather = compile_weather_data(city)
            weather_data.append(weather)
        return weather_data
    return "No cities: Add one to get started"

@weather_api.route('/weather/<int:id>', methods=['GET']) # Get city with specific id
def get_specific_city(id):
    city = City.query.get_or_404(id)
    weather = compile_weather_data(city)
    return weather

@weather_api.route('/weather', methods=['POST'])
def add_city():
    req_body = request.get_json(force=True)
    new_city = City(name=req_body.get('name'))
    db.session.add(new_city)
    db.session.commit()
    return jsonify({"id": new_city.id, "name": new_city.name})

@weather_api.route('/weather/<int:weather_id>', methods=['PUT'])
def update_city(weather_id):
    req_body = request.get_json(force=True)
    rows_counted = City.query.filter_by(id = weather_id).update(req_body)
    if rows_counted == 0: 
        abort(404)
    db.session.commit()
    return "Location with ID: " + str(weather_id) + " updated."

@weather_api.route('/weather/<int:weather_id>', methods=['DELETE'])
def del_city(weather_id):
    selected_city = City.query.get_or_404(weather_id)
    db.session.delete(selected_city)
    db.session.commit()
    return "Location with ID: " + str(weather_id) + " removed."