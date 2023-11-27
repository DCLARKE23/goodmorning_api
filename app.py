from flask import Flask, abort, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from config import WEATHER_API_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)

def get_weather(city):
    if city is None or '':
        abort(400, 'Invalid entry: null or empty string')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=" + WEATHER_API_KEY
    req = requests.get(url).json()
    return req

@app.route('/weather', methods=['GET'])
def get_cities():
    cities = City.query.all()
    weather_data = []
    if cities is not None:
        for c in cities:
            r = get_weather(c.name)
            weather = {
                'city' : c.name,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }
            weather_data.append(weather)
        return weather_data
    return "No cities: Add one to get started"

@app.route('/weather', methods=['POST'])
def add_city():
    req_body = request.get_json(force=True)
    new_city = City(name=req_body.get('name'))
    db.session.add(new_city)
    db.session.commit()
    return jsonify({"ID": new_city.id, "name": new_city.name})

@app.route('/weather/<int:weather_id>', methods=['PUT'])
def update_city(weather_id):
    req_body = request.get_json(force=True)
    rows_counted = City.query.filter_by(id = weather_id).update(req_body)
    if rows_counted == 0: 
        abort(404)
    db.session.commit()
    return "Location with ID: " + str(weather_id) + " updated."

@app.route('/weather/<int:weather_id>', methods=['DELETE'])
def del_city(weather_id):
    selected_city = City.query.get_or_404(weather_id)
    db.session.delete(selected_city)
    db.session.commit()
    return "Location with ID: " + str(weather_id) + " removed."

if __name__ == "__main__":
    app.run(debug=True)