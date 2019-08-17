import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    file = open('flights.csv');
    lines = csv.reader(file);
    for origin, destination, duration in lines:
        db.execute("INSERT INTO flights(origin, destination, duration) VALUES(:origin, :destination, :duration)",
        {"origin": origin, "destination": destination, "duration": duration})
        print(f"Flight from {origin} to {destination} lasting {duration} added successfully")
    db.commit()
            
if __name__ == "__main__":
    main()