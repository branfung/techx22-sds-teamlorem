import bcrypt
from pymongo import collection
from bson import ObjectId
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
    
def get_products(store: collection):
    products = store.find()
    return products

def get_product_by_id(id: ObjectId, store: collection):
    product = store.find_one({'_id':id})
    return product

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
        
def get_user(user: user.User, users: collection):
    user = users.find_one({'username': user.username})
    return user

def get_user_by_id(id: ObjectId, users: collection):
    user = users.find_one({'_id': id})
    return user

def add_to_cart(user: user.User, product_info: dict, users: collection,store: collection, message):
    
    product_id = ObjectId(product_info['product_id'])
    current_product = get_product_by_id(product_id, store)
    cart = get_cart(user, users)
    
    for product in cart:
        if product['product_id'] == product_id and product['size'] == product_info['size']: 

            if (product['quantity'] + product_info['quantity'] <= current_product['quantity']):
                
                # Adds onto the quantity of the already existing product in cart
                product['quantity'] += product_info['quantity']
                users.update_one({'username':user.username}, {'$set': {'cart':cart} })
                return

                
            else:
                message['error'] = "The quantity you are trying to add plus what is already on the cart exceeds what's available in stock."
                return
            
    cart.append({
        'product_id':product_id,
        'name':current_product['name'],
        'price':current_product['price'], 
        'creator':current_product['creator'],
        'quantity':product_info['quantity'],
        'image_url':current_product['image_url'],
        'size':product_info['size']
    })

    users.update_one({'username':user.username}, {'$set': {'cart':cart} })

def remove_from_cart(user: user.User, product_info: dict, users: collection):
    
    product_id = ObjectId(product_info['product_id'])
    cart = get_cart(user, users)

    
    for i, product in enumerate(cart):
        if (product['product_id'] == product_id):
            if product_info['quantity'] < product['quantity'] and product['size'] == product_info['size']:
                product['quantity'] = product['quantity'] - product_info['quantity']
                break
            elif product_info['quantity'] == product['quantity'] and product['size'] == product_info['size']:
                cart.pop(i)
                break

    users.update_one({'username':user.username}, {'$set': {'cart':cart} })

def get_cart(user: user.User, users: collection):
    cart = get_user(user, users)['cart']
    return cart

def hashed_to_star(password):
    star_pw = ""
    for char in password:
        star_pw += "*"
    # return star_pw

