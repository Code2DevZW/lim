from flask import Flask, request, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///limsusers.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)


@app.route('/')
def index():
    # check if the users exist or not
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template("register.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("index.html")


@app.route("/logout")
def logout():
    return redirect("/")


if 'name' == 'main':
    app.run(host='0.0.0.0')
