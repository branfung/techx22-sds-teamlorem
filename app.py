# -- Import section --
from flask import (Flask, render_template, request, redirect)
from flask import request, redirect, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import session
import secrets
import bcrypt
import os

# -- Initialization section --
app = Flask(__name__)

# name of database
db_name = "test"
app.config['MONGO_DBNAME'] = 'db_name'

# URI of database
password = os.environ.get('PASSWORD') # using env variables to hide sensitive info (for good practice)
app.config['MONGO_URI'] = f"mongodb+srv://admin:{password}@cluster0.pyrzd.mongodb.net/{db_name}?retryWrites=true&w=majority"

# Initialize PyMongo
mongo = PyMongo(app)

# Session Data/Cookie (secret key)
app.secret_key = secrets.token_urlsafe(16)

# -- Routes section --
# INDEX Route
@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'
    # return render_template('index.html')


# User Log in Route
# The log-in page is where the user can log into his account.
# it is going to search for the username inside the database. 
# If the username is in the database it compares the password for the user with the one provided 
# by the user. If they match the user is logged in, if they don’t let the user know the password 
# is incorrect. If the username wasn’t in the database let them know the username does not exist 
# and they need to sign in.

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        users = mongo.db.users
        # get username from database
        login_user = users.find_one({"username":request.form["username"]})

        # if user in database
        if login_user:
            password_in_db = login_user[password]
            # encode password for security purposes
            encoded_password = request.form["password"].encode("uft-8")
            # compare if the encoded password is the same as the one in the db
            if bcrypt.checkpw(password_in_db,encoded_password):
                # if we arrive here it means the password was valid
                # we store the user in the current session
                session["username"] = request.form["username"]
                return redirect(url_for('index'))
            
            else:
                return "Invalid Username or Password. Make sure the password is correct"
        else:
            return "Username not found"
    else:
        render_template("login.html")

@app.route("/logout")
def logout():
    # clear user from session
    session.clear()
    # redirect to main page
    return redirect(url_for("/"))
    

    




