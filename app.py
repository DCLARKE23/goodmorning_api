from flask import Flask
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_weather():
    data = {}
    data['lat'] = 13.1939
    data['lon'] = 59.5432
    data['appid'] = ''
    data['units'] = 'metric'
    r = requests.get('https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units={metric}&appid={appid}')
    # return render_template('index.html'), 
    return r.text

if __name__ == "__main__":
    app.run()