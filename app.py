import requests
import configparser
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cities.db'
db = SQLAlchemy(app)


class WeatherOfCities(db.Model):
    city = db.Column(db.String(100), primary_key=True, nullable=False)
    city_ascii = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    iso2 = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'City '+str(self.id)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results(cityName, apiKey):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(cityName, apiKey)
    r=requests.get(api_url)
    return r.json()

@app.route('/', methods=['GET','POST'])
def weather_dashboard():
    data = ''
    if request.method == 'POST':
        city = request.form['city']
        data = get_weather_results(city, get_api_key())
        iconUrl='hello'
        if data['weather'][0]['description']=='clear sky':
            iconUrl = 'https://cdn3.iconfinder.com/data/icons/tiny-weather-1/512/sun-256.png'
        elif data['weather'][0]['description']=='few clouds':
            iconUrl = 'https://cdn3.iconfinder.com/data/icons/tiny-weather-1/512/cloudy-256.png'
        elif data['weather'][0]['description']=='scattered clouds':
            iconUrl = 'https://cdn3.iconfinder.com/data/icons/tiny-weather-1/512/cloud-256.png'
        elif data['weather'][0]['description']=='broken clouds':
            iconUrl = 'https://cdn3.iconfinder.com/data/icons/tiny-weather-1/512/cloud-256.png'
        elif data['weather'][0]['description']=='mist' or data['weather'][0]['description']=='smoke':
            iconUrl = 'https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_30-256.png'
        elif data['weather'][0]['description']=='thunderstorm':
            iconUrl = 'https://cdn3.iconfinder.com/data/icons/tiny-weather-1/512/flash-cloud-256.png'
        elif data['weather'][0]['description']=='snow':
            iconUrl = 'https://cdn3.iconfinder.com/data/icons/tiny-weather-1/512/snow-256.png'
        else:
            iconUrl = 'https://cdn3.iconfinder.com/data/icons/tiny-weather-1/512/rain-cloud-256.png'
        

            
        print(iconUrl)
        return render_template('index.html', data=data, image=iconUrl)
    else: 
        return render_template('index.html', data=data)


@app.route('/result')
def render_results():
   return 'results'

if  __name__ == '__main__':
    app.run()




 