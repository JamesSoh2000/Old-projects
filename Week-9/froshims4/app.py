# Implements a registration form, storing registrants in a SQLite database, with support for deregistration
import sqlite3
from cs50 import SQL
from flask import Flask, redirect, render_template, request
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///froshims.db'

# db = SQL("sqlite:///froshims.db")

# db = SQLAlchemy("froshims.db")
SPORTS = [
    "Basketball",
    "Soccer",
    "Ultimate Frisbee"
]


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/deregister", methods=["POST"])
def deregister():
    con = sqlite3.connect("froshims.db")
    db = con.cursor()

    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
        con.commit()
    return redirect("/registrants")
    con.close()


@app.route("/register", methods=["POST"])
def register():
    con = sqlite3.connect("froshims.db")
    db = con.cursor()

    # Validate submission
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")

    # Remember registrant
    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", (name, sport))
    con.commit()
    # Confirm registration
    return redirect("/registrants")
    con.close()

@app.route("/registrants")
def registrants():
    con = sqlite3.connect("froshims.db")
    con.row_factory = sqlite3.Row
    db = con.cursor()

    db.execute("SELECT * FROM registrants")
    registrants = db.fetchall();


    return render_template("registrants.html", registrants=registrants)
    con.close()

