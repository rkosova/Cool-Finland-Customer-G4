from flask import Flask, render_template, url_for, flash, redirect, request
import sqlite3
from passlib.hash import bcrypt
from forms import RegistrationForm, LoginForm

app = Flask(__name__, static_url_path='/static')

#secret key is for app security to protect from attacks
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

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
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
