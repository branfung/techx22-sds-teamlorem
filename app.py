# -- Import section --
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from model import (
    model,
    product,
    user
)
from flask_pymongo import PyMongo
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


'''
The Request Design route
In here the user can create and request their design to be sold on our store using the provided form.
The user must provide a valid URL of the image that will represent their design.
'''
@app.route('/request', methods=['GET', 'POST'])
def request_design():
    if request.method == 'POST':
        
        message = {'message': '', 'error': None}
        
        new_product = product.make_product({
            'name': request.form['name'].capitalize(),
            'price': round(float(request.form['price']), 2),
            'creator': session['username'],
            'quantity': int(request.form['quantity']),
            'image_url': request.form['image_url']
        }, message)
        
        if not message['error']:            
            store = mongo.db.store
            model.add_product(new_product, store, message)
        
        return render_template('request-form.html', session=session, message=message)
    else:
        return render_template('request-form.html', session=session)


'''
The sign up route checks if the given email or username exists, if it does it renders an error message
stating the email or user is already in use. Otherwise it adds the user to the database and 
logs in to their account. 
'''
@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        
        message = {'message': '', 'error': None}

        new_user = user.make_user({
            'email': request.form['email'],
            'username': request.form['username'],
            'password': request.form['password'],
        })
        
        users = mongo.db.users
        model.add_user(new_user, users, message)
        if message['error']:
            return render_template('Sign-Up.html', session=session, message=message)

        session['username'] = new_user.username
        return redirect(url_for('index'))

    else:
        if session.get('username'):
            return redirect(url_for('index'))
        return render_template('Sign-Up.html')

'''
User Log in Route
The log-in page is where the user can log into their account.
it is going to search for the username inside the database. 
If the username is in the database it compares the password for the user with the one provided 
by the user. If they match the user is logged in, if they don’t let the user know the password 
is incorrect. If the username wasn’t in the database let them know the username does not exist 
and they need to sign in.
'''
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        message = {'message': '', 'error': None}

        user_auth = user.make_user({
            'email': 'TO_LOGIN',
            'username': request.form['username'],
            'password': request.form['password'],
        })
        
        users = mongo.db.users
        model.authenticate_user(user_auth, users, message)
        if message['error']:
            return render_template("login.html", session=session, message=message)
        
        session['username'] = user_auth.username
        return redirect(url_for('index'))
    
    else:
        if session.get('username'):
            return redirect(url_for('index'))
        return render_template("login.html", session=session)

@app.route("/logout")
def logout():
    # clear user from session
    session.clear()
    return redirect(url_for("index"))


'''
The buy route gets all the items that are in the database and renders them in the 
buy.html page so users can choose what they want to buy.
'''
@app.route('/buy')
def buy():
    store = mongo.db.store
    products = model.get_products(store)
    return render_template('buy.html', store_items=products)


'''
The add to cart function looks for the item the user wants to buy inside the database.
Then if the item is already in the cart it updates it's value if what's in the cart and the amount 
they want to add is less than or equal to what is in stock. If not it renders an error.
Else if the item wasn't in the cart or if it's in the cart with a differnt size the item gets added to the cart.
'''
@app.route("/addtocart", methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    size = request.form['size']
    username = session['username']
    users = mongo.db.users
    store = mongo.db.store
    current_product = store.find_one({'_id':ObjectId(product_id)})
    current_user = users.find_one({"username":username})
    cart = current_user['cart']

    if not cart:
        cart.append({'product_id':product_id, 'name':current_product['name'], 'price':current_product['price'], 
        'creator':current_product['creator'], 'quantity':quantity, 'image_url':current_product['image_url'], 'size':size})
    
    else: 
        for item in cart:
            if item['product_id'] == product_id:

                if (item['quantity'] + quantity <= current_product['quantity']) and (item['size'] == size):
                    item['quantity'] = item['quantity'] + quantity
                    users.update_one({'username':username}, {'$set': {'cart':cart} })
                    return redirect(url_for('buy'))

                elif item['size'] != size:
                    cart.append({'product_id':product_id, 'name':current_product['name'], 'price':current_product['price'], 
                    'creator':current_product['creator'], 'quantity':quantity, 'image_url':current_product['image_url'], 'size':size})
                    users.update_one({'username':username}, {'$set': {'cart':cart} })
                    return redirect(url_for('buy'))
                
                else:
                    error_message = "The quantity you are trying to add plus what is already on the cart exceeds what's available in stock"
                    return render_template('buy.html', error_message=error_message)
        
        cart.append({'product_id':product_id, 'name':current_product['name'], 'price':current_product['price'], 
        'creator':current_product['creator'], 'quantity':quantity, 'image_url':current_product['image_url'], 'size':size})

    users.update_one({'username':username}, {'$set': {'cart':cart} })
    return redirect(url_for('buy'))



'''
The show cart route gets the cart associated with the user that's logged in and displays all the items 
inside it. 
'''
@app.route('/showcart', methods=['GET'])
def show_cart():
    username = session['username']
    users = mongo.db.users
    current_user = users.find_one({"username":username})
    cart_items = current_user['cart']
    return render_template('cart.html', items=cart_items)



'''
The remove route gets the id of the product that the user wants to remove and searches for it in the cart.
Then either reduces the quantity of the item as selected by the user or removes it complety if the 
quantity selected by the user equals the amount that is present in the cart.  
'''
@app.route('/remove', methods=['POST'])
def remove():
    product_id = request.form['product_id']
    quantity_to_be_removed = int(request.form['quantity'])
    size = request.form['size']
    username = session['username']
    users = mongo.db.users
    current_user = users.find_one({"username":username})
    cart = current_user['cart']
 
    for i,element in enumerate(cart):
        if (element['product_id'] == product_id):
            if quantity_to_be_removed < element['quantity'] and element['size'] == size:
                element['quantity'] = element['quantity'] - quantity_to_be_removed
                break
            elif quantity_to_be_removed == element['quantity'] and element['size'] == size:
                cart.pop(i)
                break

    users.update_one({'username':username}, {'$set': {'cart':cart} })
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

@app.route("/account", methods=["GET","POST"])
# this router shall be only available if a user is logged in
def account():
    if request.method =="POST":
        # get the user from the db
        users = mongo.db.users
        # save the current user to modify its info
        # current_user = users.find_one({"username":session.get("USERNAME")})
        current_user = users.find_one({"username":session.get("USERNAME")})

        new_firstname = {"$set":{"firstname":request.form["firstname"]}}
        users.update_one({"username":session.get("USERNAME")},new_firstname)

        new_lastname = {"$set":{"lastname":request.form["lastname"]}}
        users.update_one({"username":session.get("USERNAME")},new_lastname)

        return render_template("account.html", firstname=users.find_one({"username":session.get("USERNAME")}),lastname=users.find_one({"username":session.get("USERNAME")}))

    else:
        if session.get('username'):
            return redirect(url_for('login'))
        return render_template("account.html")



if __name__ == "__main__":
        app.run()
