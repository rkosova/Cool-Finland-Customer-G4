from flask import Flask, request, redirect, render_template
import sqlite3
from passlib.hash import bcrypt

app = Flask(__name__, static_url_path='/static')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def login_val(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    users = conn.execute('select * from "users"').fetchall()
    conn.close()

    hasher = bcrypt.using(rounds=13)

    for user in users:
        if user["email"] == username:
            if hasher.verify(password, user["password"]):
                return True

    return False


def email_in(email, conn):
    emails = conn.execute('select email from "users"').fetchall()

    for email_ in emails:
        if email_ == email:
            return True

    return False


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
        username = request.form.get('email')
        h_passw = request.form.get('password')
        logged = login_val(username, h_passw)

        if logged:
            return render_template("index.html")
        else:
            return render_template("login.html.jinja", error=not logged)
    else:
        return render_template("login.html.jinja", error=None)




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        passw = request.form.get('password')
        c_name = request.form.get('cname')
        rep_name = request.form.get('rep_n')
        rep_lname = request.form.get('rep_ln')
        rep_pnum = request.form.get('rep_pn')

        hasher = bcrypt.using(rounds=13)
        h_passw = hasher.hash(passw)

        conn = get_db_connection()
        cur = conn.cursor()
        valid_email = not email_in(email, conn)
        if valid_email:
            conn.execute(
                'insert into "users" (email, password, comp_name, rep_name, rep_lname, rep_pnumber) values (?, ?, ?, ?, ?, ?)',
                (email, h_passw, c_name, rep_name, rep_lname, rep_pnum))
            conn.commit()
            conn.close()
            return redirect("/")
        else:
            conn.close()
            return render_template("register.html.jinja", error=not valid_email)
    else:
        return render_template("register.html.jinja")


@app.route("/schedule")
def schedule():
    return render_template("schedule.html")
