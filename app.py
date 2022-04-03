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
from form import SignUpForm
from bson.objectid import ObjectId
import gunicorn
import requests
import secrets
import os, secrets
import bcrypt 
import certifi
import os

# -- Initialization section --
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(nbytes=16)

# name of database
db_name = 'test' if os.environ.get('DB_TEST') == '1' else 'PopulusDesigns'
app.config['MONGO_DBNAME'] = db_name

# URI of database
password = os.environ.get('PASSWORD') # using env variables to hide sensitive info (for good practice)
app.config['MONGO_URI'] = f"mongodb+srv://admin:{password}@cluster0.pyrzd.mongodb.net/{db_name}?retryWrites=true&w=majority"

# Initialize PyMongo
mongo = PyMongo(app, tlsCAFile=certifi.where())

# Session Data/Cookie (secret key)
app.secret_key = secrets.token_urlsafe(16)

# -- Routes section --
# INDEX Route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', session=session)

@app.route('/request', methods=['GET', 'POST'])
def request_design():
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


# Do we create a User class or store the information as is inside the data base ? 
@app.route('/signup', methods=['GET','POST'])
def signup():
    sign_up_form = SignUpForm()
    if request.method == 'POST':
        if sign_up_form.validate_on_submit():
            
            users = mongo.db.users
            email = request.form['email']
            username = request.form['username']
            existing_user = users.find_one(filter={"username":username})
            
            if existing_user:
                return render_template('Sign-Up.html', session=session, existing_user=existing_user)

            password = request.form['password'].encode('utf-8')
            salt = bcrypt.gensalt()
            hased_pasword = bcrypt.hashpw(password, salt)
            users.insert_one({'username':username, 'password':hased_pasword, 'cart':[]})
            session['username'] = username

            return redirect(url_for('index'))
    else:
        return render_template('Sign-Up.html', session=session, form=sign_up_form)

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
            password_in_db = login_user["password"]
            # encode password for security purposes
            encoded_password = request.form["password"].encode("utf-8")
            # compare if the encoded password is the same as the one in the db
            if bcrypt.checkpw(encoded_password,password_in_db):
                # if we arrive here it means the password was valid
                # we store the user in the current session
                session["username"] = request.form["username"]
                return redirect(url_for('index'))
            
            else:
                return render_template("login.html",session=session, error_message="Password is incorrect")
        else:
            return render_template("login.html",session=session, error_message="Username is incorrect")
    else:
        return render_template("login.html", session=session)

@app.route("/logout")
def logout():
    # clear user from session
    session.clear()
    # redirect to main page
    return redirect(url_for("index"))

@app.route('/buy', methods=['GET','POST'])
def buy():
    collection = mongo.db.store
    store_items = collection.find({})
    return render_template('buy.html', session=session, store_items=store_items)

@app.route("/addtocart", methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    # username = session["username"]
    username = 'petraca'
    users = mongo.db.users
    store = mongo.db.store
    current_product = store.find_one({'_id':ObjectId(product_id)})
    current_user = users.find_one({"username":username})
    cart = current_user['cart']

    cart.append({'product_id':product_id, 'name':current_product['name'], 'price':current_product['price'], 
                'creator':current_product['creator'], 'quantity':quantity, 'image_url':current_product['image_url']})
    
    users.update_one({'username':username}, {'$set': {'cart':cart} })
    return redirect(url_for('buy'))

@app.route('/showcart', methods=['GET'])
def show_cart():
    # username = session["username"]
    users = mongo.db.users
    current_user = users.find_one({"username":'petraca'})
    # cart = current_user['cart']
    cart_items = current_user['cart']
    return render_template('cart.html', session=session, items=cart_items)

@app.route('/remove', methods=['POST'])
def remove():
    product_id = request.form['product_id']
    users = mongo.db.users
    current_user = users.find_one({"username":'petraca'})
    cart = current_user['cart']
    index = 0
    for i,element in enumerate(cart):
        if element['product_id'] == product_id:
            index = i
    print(index)
    cart.pop(index)
    users.update_one({'username':'petraca'}, {'$set': {'cart':cart} })
    return redirect(url_for('show_cart'))

# Allow the user to reset/change its password
@app.route("/resetpw",methods=["GET","POST"])
def resetpw():
    users = mongo.db.users
    if request.method == "GET":
        return render_template("changepw.html", session=session)
    else:
        # update old password with new password
        if users.find_one({"username":request.form["username"]}):
            username = request.form["username"]
             # obtain new password and encrypt it for security reasons
            password = request.form['password'].encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_pasword = bcrypt.hashpw(password, salt)
            newvalue = {"$set": { "password": hashed_pasword }}
            # update user's old password with new password
            users.update_one({"username":username}, newvalue)
            # go back to index page
            return redirect("/login")
        else:
            return render_template("changepw.html", session=session, error_message="Username not found")
            # return render_template("login.html", error_message="Username is incorrect")

@app.route('/about')
def about():
    return render_template('about.html', session=session)


if __name__ == "__main__":
        app.run()