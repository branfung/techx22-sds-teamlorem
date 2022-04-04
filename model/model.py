import bcrypt
from pymongo import collection
from model.objects import (
    product,
    user
) 

# TODO: Create model components

def add_product(product: product.Product, store: collection, message):
    '''Adds a Product to the store collection'''
    
    # DB insert_one error handling
    try:
        store.insert_one(product.to_document())
        message['message'] = 'Your design was uploaded succesfully!'
    except:
        message['error'] = 'Could not upload design. Please make sure the fields are correct or try again some other time'
    
    
def add_user(user: user.User, users: collection, message):
    """Adds a User to the users collection
    """
    
    # Checking for existing email/username
    existing_email = users.find_one({'email': user.email})
    if existing_email:
        message['error'] = 'A user with that email address already exists. Try logging in or creating a new account.'
        return
    
    existing_username = users.find_one({'username': user.username})
    if existing_username:
        message['error'] = 'That username already exists. Try login or choosing a different username.'
        return
    
    # DB insert_one error handling
    try:
        
        users.insert_one(user.to_document())
    except:
        message['error'] = 'Could not sign up. Please make sure the fields are correct or try again some other time'
    
def authenticate_user(user: user.User, users: collection, message):
    """Retrieves  user from the database"""
    
    # get username from database
    login_user = users.find_one({"username": user.username})

    # if user in database
    if login_user:
        password_in_db = login_user["password"]
        # encode password for security purposes
        encoded_password = user.password.encode("utf-8")
        # compare if the encoded password is the same as the one in the db
        if not bcrypt.checkpw(encoded_password,password_in_db):
            # if we arrive here it means the password was valid
            # we store the user in the current session
            message['error'] = 'Password is incorrect'
    else:
        message['error'] = 'This user does not exist'

def get_products(store: collection):
    products = store.find()
    return products

# def get_product()