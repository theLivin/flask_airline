import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book",methods=["POST"])
def book():
    '''Book a flight'''

    #Get form information
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid Flight Number")

    #Make sure the flight exists
    if db.execute("SELECT * FROM flights WHERE id=:id", {"id": flight_id}).fetchone() == None:
        return render_template("error.html", message="No such flight with that id")
    #Make booking
    db.execute("INSERT INTO passengers(name, flight_id) VALUES(:name, :id)", {"name": name, "id": flight_id})
    db.commit()
    return render_template("success.html")

@app.route("/flights")
def flights():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html", flights=flights)
    
@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    flight = db.execute("SELECT * FROM flights WHERE id=:id", {"id": flight_id}).fetchone()
    if flight is None:
        return render_template("error.html", message="No such flight")
    passengers = db.execute("SELECT name FROM passengers WHERE flight_id=:flight_id",
    {"flight_id": flight_id}).fetchall()
    return render_template("flight.html",flight=flight,passengers=passengers)
    
if __name__ == "__main__":
    app.run(debug=True)