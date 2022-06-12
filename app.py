from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import psycopg2
import os
import hashlib

app = Flask(__name__)
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///limsusers.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

user = None
# connecting to posgress database


def get_db_connection():
    conn = psycopg2.connect(host="127.0.0.1",
                            port="5433",
                            database="lims_users",
                            user=os.environ['DB_USER'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@ app.route('/')
def index():
    return render_template('index.html')


@ app.route('/features')
def features():
    return render_template('features.html', user=user)


@ app.route('/faqs')
def faqs():
    return render_template('faqs.html', user=user)


@ app.route('/about')
def about():
    return render_template('about.html', user=user)


@ app.route('/contact')
def contact():
    # check if the users exist or not
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return render_template('contact.html')


@ app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        password = hashlib.sha3_512(password.encode(
            encoding='UTF-8', errors='strict')).hexdigest()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name, surname, email, password)'
                    'VALUES (%s, %s, %s, %s)',
                    (name, surname, email, password))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('login'))


@ app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/cadastre")
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        password = hashlib.sha3_512(password.encode(
            encoding='UTF-8', errors='strict')).hexdigest()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        print(user[4])
        print(password)
        if user:
            if user[4] == password:
                session["name"] = hashlib.sha512(email.encode(
                    encoding='UTF-8', errors='strict')).hexdigest()
                return redirect(url_for('cadastre'))
            else:
                print("error")
            return render_template("login.html")
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("login.html")


@ app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


@ app.route("/cadastre")
def cadastre():
    email = session.get("name")
    print(email)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("cadastre.html", user=user)


@ app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')


if 'name' == 'main':
    print("Please ntocie me", request.environ['SERVER_NAME'])
    app.run(debug=True, host='0.0.0.0')
