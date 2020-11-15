import requests
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()
    weather_data=[]
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ENTER API TOKEN HERE'
    
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        if r['cod'] != '404':
            icon_url = 'http://api.openweathermap.org/img/w/{}.png'.format(r['weather'][0]['icon'])
            weather = {
                'city': city.name,
                'desc': r['weather'][0]['description'],
                'temp': r['main']['temp'],
                'icon': icon_url,
            }

            weather_data.append(weather)
    return render_template('index.html', weather_data = weather_data)



if __name__ == '__main__':
    port = int(os.environ.get("port",5000))
    app.run(host='1.0.0.0', port=port)
