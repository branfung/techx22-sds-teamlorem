# -- Import section --
from flask import (Flask, render_template, request, redirect)
from flask_pymongo import PyMongo
import os

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database
password = os.environ.get('PASSWORD') # using env variables to hide sensitive info (for good practice)
app.config['MONGO_URI'] = f"mongodb+srv://admin:{password}@cluster0.pyrzd.mongodb.net/database?retryWrites=true&w=majority"

#Initialize PyMongo
mongo = PyMongo(app)

# -- Routes section --
# INDEX Route
@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'
    # return render_template('index.html')