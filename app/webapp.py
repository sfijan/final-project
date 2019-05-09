#!/home/sven/Documents/fer/zavrsni/venv/bin/python

from flask import Flask, render_template, url_for
from models import *
import datetime
app = Flask(__name__)

database.connect()


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/calendar")
def calendar():
    competitions = Competition.select()
    return render_template('calendar.html', title='calendar', competitions=competitions)

if __name__ == '__main__':
    app.run(debug=True)
