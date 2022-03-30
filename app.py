# -- Import section --
from flask import (Flask, render_template, request, redirect, url_for)
from flask_pymongo import PyMongo
import os

# -- Initialization section --
app = Flask(__name__)

# name of database
db_name = 'test'
app.config['MONGO_DBNAME'] = db_name

# URI of database
password = os.environ.get('PASSWORD') # using env variables to hide sensitive info (for good practice)
app.config['MONGO_URI'] = f"mongodb+srv://admin:{password}@cluster0.pyrzd.mongodb.net/{db_name}?retryWrites=true&w=majority"

#Initialize PyMongo
mongo = PyMongo(app)

# -- Routes section --
# INDEX Route
@app.route('/')
@app.route('/index')
def index():
    store = mongo.db.store.find({})
    return render_template("index.html", store=store)