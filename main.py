from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager
#SQL Alchemy is great for representing data from the db as models(classes) 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from passlib.hash import bcrypt
from forms import RegistrationForm, LoginForm

app = Flask(__name__, static_url_path='/static')

#secret key is for app security to protect from attacks
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Creating an instance of database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Creating class User to hold information in the db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.image_file}')"



@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    #taking RegistrationForm from forms.py
    form = RegistrationForm()
    #Loop to check if the account has been successfuly generated, from SQLAlchemy
    if form.validate_on_submit():
        #hashing the password that we get from Registrationform
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #creating an instance of user class to input into the db
        user = User(email=form.email.data, password=hashed_password)
        #adding user to the db
        db.session.add(user)
        #comitting session
        db.session.commit()
        #flashing a notification about account creation
        flash('Your account has been created! You are now able to log in', 'success')
        #taking user to login page after successful reg
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
