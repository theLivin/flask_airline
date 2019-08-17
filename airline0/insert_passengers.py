import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    file = open("passengers.csv")
    reader = csv.reader(file)
    for name, flight_id in reader:
        db.execute("INSERT INTO passengers(name, flight_id) VALUES(:name, :flight_id)",
        {"name": name, "flight_id": flight_id})
        print(f"{name} has been added to flight with id {flight_id}")
    db.commit()

if __name__ == "__main__":
    main()