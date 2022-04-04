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
    except:
        message['error'] = 'Could not upload design. Please make sure the fields are correct or try again some other time'
        return
    
    # Product insert success:
    message['message'] = 'Your design was uploaded succesfully!'
    
def add_user(user: user.User, users: collection, message):
    pass

def hashed_to_star(password):
    star_pw = ""
    for char in password:
        star_pw += "*"
    # return star_pw
