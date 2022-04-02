# -- Import section --
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from flask_pymongo import PyMongo
import requests
import secrets
import bcrypt
import os

# -- Initialization section --
app = Flask(__name__)

# name of database
db_name = "test"
app.config['MONGO_DBNAME'] = db_name

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
    store = mongo.db.store.find()
    return render_template('index.html', session=session, store=store)

@app.route('/request', methods=['GET', 'POST'])
def upload_design():
    if request.method == 'POST':
        message = {'message': '', 'error': None}
        # session['username'] = 'Brandon' 
        
        # Fetching the image_url from the user to check if it gives us headers        
        print(dict(request.form))    
        try:
            url = request.form['image_url']
            response = requests.get(url)
        except:
            message['error'] = 'Something went wrong with your image URL'
            return render_template('request-form.html', session=session, message=message)

        # Validating image_url to see if it's an image
        if response.headers.get('content-type') not in ['image/png', 'image/jpeg']:
            message['error'] = 'URL is not a valid image URL! Please use a correct URL'
            return render_template('request-form.html', session=session, message=message)
        
        # Constructing product object
        product = {
            'name': request.form['name'],
            'price': round(float(request.form['price']), 2),
            'creator': session['username'],
            'quantity': int(request.form['quantity']),
            'image_url': request.form['image_url']
        }
        # session.clear()
        # print(product)
        
        # DB insert_one error handling
        try:
            store = mongo.db.store
            store.insert_one(product)  
            # print('Product added')
        except:
            message['error'] = 'Could not upload design. Please make sure the fields are correct or try again some other time'
            return render_template('request-form.html', session=session, message=message)
        
        # Product insert success:
        message['message'] = 'Your design was uploaded succesfully!'
        return render_template('request-form.html', session=session, message=message)
    else:
        return render_template('request-form.html', session=session)


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
        return render_template("login.html")

@app.route("/logout")
def logout():
    # clear user from session
    session.clear()
    # redirect to main page
    return redirect(url_for("/"))
    

