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
import gunicorn # for heroku deployment
import secrets
import bcrypt 
import certifi
import os

# -- Initialization section --
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(nbytes=16)

# Name of database
db_name = 'test' if os.environ.get('DB_TEST') == '1' else 'PopulusDesigns'
app.config['MONGO_DBNAME'] = db_name

# URI of database
password = os.environ.get('PASSWORD') # using env variables to hide sensitive info (for good practice)
app.config['MONGO_URI'] = f"mongodb+srv://admin:{password}@cluster0.pyrzd.mongodb.net/{db_name}?retryWrites=true&w=majority"

# Initialize PyMongo
mongo = PyMongo(app, tlsCAFile=certifi.where())

# Collection References
store = mongo.db.store
users = mongo.db.users

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
by the user. If they match the user is logged in, if they don't let the user know the password 
is incorrect. If the username wasn't in the database let them know the username does not exist 
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
        
        model.authenticate_user(user_auth, users, message)
        if message['error']:
            return render_template("login.html", session=session, message=message['error'])
        
        session['username'] = user_auth.username
        return redirect(url_for('index'))
    
    else:
        if session.get('username'):
            return redirect(url_for('index'))
        return render_template("login.html", session=session)

"""
Method that allows the user to logout their account from the page's current session
Returns:
    redirects user to main page (index.html) with their account logged out
"""
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
    message = {'message': '', 'error': None}

    if not session.get('username'):
        return redirect(url_for('index'))
    
    current_user = user.make_user({
        'email':'GET_USER',
        'username': session.get('username'),
        'password':'GET_USER'
    })

    info = {
        'product_id': request.form['product_id'],
        'quantity': int(request.form['quantity']),
        'size': request.form['size']
    }
    
    model.add_to_cart(current_user, info, users, store, message)  
    
    if message['error']:
        return render_template('buy.html', message=message)     
    
    return redirect(url_for('buy'))



'''
The show cart route gets the cart associated with the user that's logged in and displays all the items 
inside it. 
'''
@app.route('/showcart')
def show_cart():
    
    if session.get('username'):
        
        current_user = user.make_user({
            'email':'GET_USER',
            'username': session.get('username'),
            'password':'GET_USER'
        })

        cart = model.get_cart(current_user, users)
        return render_template('cart.html', items=cart)
    else:
        return redirect(url_for('index'))



'''
The remove route gets the id of the product that the user wants to remove and searches for it in the cart.
Then either reduces the quantity of the item as selected by the user or removes it complety if the 
quantity selected by the user equals the amount that is present in the cart.  
'''
@app.route('/remove', methods=['POST'])
def remove():    
    if not session.get('username'):
        return redirect(url_for('index'))
    
    current_user = user.make_user({
        'email':'GET_USER',
        'username': session.get('username'),
        'password':'GET_USER'
    })

    info = {
        'product_id': request.form['product_id'],
        'quantity': int(request.form['quantity']),
        'size': request.form['size']
    }

    model.remove_from_cart(current_user, info, users)
 
    return redirect(url_for('show_cart'))

"""
Allows the user to reset or change their current password to a new one
For now, the only validation is the username since these are unique
More validation is needed for the future

Returns:
    If sucessful, returns user to login page, else the user made a mistake
    (user not found) and it throws an error for the user to see
"""
@app.route("/resetpw",methods=["GET","POST"])
def resetpw():
    # get users db
    users = mongo.db.users
    if request.method == "GET":
        return render_template("changepw.html", session=session)
    else:
        # update old password with new password
        current_user = users.find_one({"username":session["username"]})
        if users.find_one({"username":session["username"]}):
            current_user = session["username"]
            username = request.form["username"]
            if current_user == username:
                # obtain new password and encrypt it for security reasons
                password = request.form['password'].encode('utf-8')
                salt = bcrypt.gensalt()
                hashed_pasword = bcrypt.hashpw(password, salt)
                # set the new value of the password
                newvalue = {"$set": { "password": hashed_pasword }}
                # update user's old password with new password
                users.update_one({"username":username}, newvalue)
                # go back to index page
                return redirect("/login")
            else:
                return render_template("changepw.html",session=session,error_message="Inccorect User")
        else:
            return render_template("changepw.html", session=session, error_message="Username not Correct")
            # return render_template("login.html", error_message="Username is incorrect")

"""
Renders the About page, where the user can get to know more about us as a company.
"""
@app.route('/about')
def about():
    return render_template('about.html', session=session)

"""
Allows the user to modify their account and profile and the option to delete
their account and connect to different platforms

Returns:
    JinjaTemplate: renders the same page again with all the changed made present.
    It can also redirect to delete the account.
"""
@app.route("/account", methods=["GET","POST"])
# this router shall be only available if a user is logged in
def account():
    # get the user from the db
    users = mongo.db.users
    # save the current user to modify its info
    current_user = session['username']
    # save the document from the DB that represents the current user in the page
    user_doc = users.find_one({"username":current_user})

    if request.method =="POST":

        try:
            option = request.form["delete"]
            if option == "yes":
                return redirect("/delete-account")
        except:
            pass
        
        # get the input firstname from the form in order to update it
        new_firstname = {"$set":{"firstname":request.form["firstname"]}}
        users.update_one({"username":current_user},new_firstname)

        # get the input lastame from the form in order to update it
        new_lastname = {"$set":{"lastname":request.form["lastname"]}}
        users.update_one({"username":current_user},new_lastname)

        # get the input bio from the form in order to update it
        new_bio = {"$set":{"bio":request.form["bio"]}}
        users.update_one({"username":current_user},new_bio)

        user_doc = users.find_one({"username":current_user})

        # return render_template("account.html", session=session,firstname=user_doc["firstname"],
        # lastname=user_doc["lastname"],bio=user_doc["bio"],
        # password=model.hashed_to_star(user_doc["password"]))
    
    

    # load account info with the one prev found in the user's document
    try:
        return render_template("account.html", session=session,
        firstname=user_doc["firstname"],lastname=user_doc["lastname"],
        bio=user_doc["bio"],password=model.hashed_to_star(user_doc["password"]),
        email=user_doc["email"])
    except:
        return render_template("account.html",firstname="",lastname="",bio="",
        password="******",session=session)

"""
Delete the users account from the users data base 

Redirects to the logout where the account is also cleared from the current session
and it is redirected to the main page (index.html)
"""
@app.route("/delete-account",methods=["GET","POST"])
def delete_account():
    if request.method == "POST":
        users = mongo.db.users
        users.delete_one({"username":session["username"]})
        return redirect("/logout")
    else:
        if session.get('username'):
            return redirect(url_for('login'))
        return render_template("account.html")

"""
Allows the user to change their current email to a new one
For now, the only validation is the username since these are unique
More validation is needed for the future

Returns:
    If sucessful, returns user to login page, else the user made a mistake
    (user not found) and it throws an error for the user to see
"""
@app.route("/change-email",methods=["GET","POST"])
def change_email():
    # get users db
    users = mongo.db.users
    if request.method == "GET":
        return render_template("changeemail.html", session=session)
    else:
        # update old password with new password
        current_user = users.find_one({"username":session["username"]})
        if users.find_one({"username":session["username"]}):
            current_user = users.find_one({"username":session["username"]})
            username = request.form["username"]
            if current_user["username"] == username:
                new_email = request.form["email"]
                # set the new value of the password
                newvalue = {"$set": { "password": new_email }}
                # update user's old password with new password
                users.update_one({"username":username}, newvalue)
                # go back to index page
                return redirect("/login")
            else:
                return render_template("changeemail.html", session=session, error_message="Incorrect User")
        else:
            return render_template("changeemail.html", session=session, error_message="Username not found")



if __name__ == "__main__":
        app.run()
