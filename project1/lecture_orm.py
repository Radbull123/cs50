# import os
# import csv
# from flask import Flask, session
# from flask_session import Session
# from create_db import db, Flight, Passenger, Pilot
#
#
# app = Flask(__name__)
#
# # Check for environment variable
# if not os.getenv("SQLALCHEMY_DATABASE_URI"):
#     os.environ["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost:5432/postgres"
#     # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
# app.config["SESSION_TYPE"] = "filesystem"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Session(app)
#
# # Set up database
# # engine = create_engine(os.getenv("DATABASE_URL"))
# # db = scoped_session(sessionmaker(bind=engine))
# db.init_app(app)
#
#
# def main():
#     # with open("flights.csv") as flights_result:
#     #     flights_csv = csv.reader(flights_result)
#     #     for origin, destination, duration in flights_csv:
#     #         if Flight.query.filter_by(origin=origin, destination=destination).first() is None:
#     #             Flight(origin=origin, destination=destination, duration=duration)
#     # db.session.commit()
#     db.create_all()
#
#
# @app.route("/")
# def index():
#     return "Project 1: TODO"
#
#
# if __name__ == "__main__":
#     app.run()
