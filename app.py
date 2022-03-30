# -- Import section --
from flask import (Flask, render_template, request, redirect, url_for, session)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
import os, secrets
from form import SignUpForm
import bcrypt 
import certifi

# -- Initialization section --
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(nbytes=16)

# name of database
app.config['MONGO_DBNAME'] = 'test'

# URI of database
password = os.environ.get('PASSWORD') # using env variables to hide sensitive info (for good practice)
app.config['MONGO_URI'] = "mongodb+srv://admin:fm3EdoNvRAhOLW22@cluster0.pyrzd.mongodb.net/test?retryWrites=true&w=majority"

#Initialize PyMongo
mongo = PyMongo(app, tlsCAFile=certifi.where())

# -- Routes section --
# INDEX Route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Do we create a User class or store the information as is inside the data base ? 
@app.route('/signup', methods=['GET','POST'])
def signup():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        
        users = mongo.db.users
        email = request.form['email']
        username = request.form['username']
        existing_user = users.find_one(filter={"username":username})
        
        if existing_user:
            return render_template('Sign-Up.html', existing_user=existing_user)

        password = request.form['password'].encode('utf-8')
        salt = bcrypt.gensalt()
        hased_pasword = bcrypt.hashpw(password, salt)
        users.insert_one({'username':username, 'password':hased_pasword})
        session['username'] = username

        return redirect(url_for('index'))
    return render_template('Sign-Up.html', form=sign_up_form)

@app.route('/buy', methods=['GET','POST'])
def buy():
    pass

@app.route('/login', methods=['POST'])
def login():
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    return render_template('log-in.html', email=email, username=username, password=password)