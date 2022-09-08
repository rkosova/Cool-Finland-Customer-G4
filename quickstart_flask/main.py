from flask import Flask, request, render_template, url_for, redirect
from markupsafe import escape
import sqlite3

app = Flask(__name__, static_url_path='/static')

#@app.route("/")
# @app.route("/hello/")
# def hello(name=None):
# 	return render_template("hello.html.jinja", name=name)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/admin")
def admin():
	conn = get_db_connection()
	cur = conn.cursor()
	users = conn.execute('select * from "users"').fetchall()
	conn.close()
	return render_template("admin.html.jinja", users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get('username')
		password = request.form.get('password')
		return render_template("login_test.html.jinja", username=username, password=password)
	else:
		return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		email = request.form.get('email')
		passw = request.form.get('password')
		conn = get_db_connection()
		cur = conn.cursor()
		conn.execute('insert into "users" (email, password) values (?, ?)', (email, passw))
		conn.commit()
		conn.close()
		return redirect("/")
	else:
		return render_template("register.html")
