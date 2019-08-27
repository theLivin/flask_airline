import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html",flights=flights)

@app.route("/book", methods=["POST"])
def book():
    '''Book a flight'''
    #Get the name from the form
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid Flight Number")
        
    #Make sure flight exists
    if Flight.query.get(flight_id) == None:
        return render_template("error.html", message="No such flight with that id")
        
    #Make booking
    passenger = Passenger(name=name, flight_id=flight_id)
    db.session.add(passenger)
    db.session.commit()
    return render_template("success.html")

@app.route("/flights")
def flights():
    flights = Flight.query.all()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    flight = Flight.query.get(flight_id)
    if flight == None:
        return render_template("error.html", message="No such flight")
        
    #passengers = flight.passengers
    #alternatively,
    passengers = Passenger.query.filter_by(flight_id=flight_id).all()
    return render_template("flight.html", flight=flight, passengers=passengers)


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
