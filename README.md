# For Unit 3 Project
## Setup: 
In order to run the app in vscode, run the following commands:
- ``python3 -m venv venv`` to setup a python virtual environment.
- For Windows: ``./venv/Scripts/activate`` to run the *venv*.
- For MacOS/Linux ``. /venv/bin/activate`` to run the *venv*

**Sidenote:** To exit out of the *venv*, type ``deactivate``. 
## Install packages:
To install a python package do ``pip install <package_name>``

Install the following packages inside the *venv*:
- ``flask``
- ``flask-pymongo``
- ``dnspython``
- ``python-dotenv``
- ``flask-wtf``
- ``email_validator``
- ``certifi``
- ``bcrypt``
- ``requests``

Or install them in one command with ``pip install flask flask-pymongo dnspython python-dotenv flask-wtf email_validator certifi bcrypt``.

## Run the app:
``flask run`` to run the app while the *venv* is active

**Note:** Always run the command after doing ``.venv/<Scripts or bin>/activate``
