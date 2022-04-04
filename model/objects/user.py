import bcrypt

class User:
    
    def __init__(self, email: str, username: str, password: str):
        """Creates a user that can be used to create a session.
        

        Args:
            email (str): The email address of the user
            username (str): The username of the user
            password (str): The password of the user.

        """
                
        if type(email) != str: raise TypeError('Email must be a string')
        if email == '' or email.isspace(): raise ValueError('Email must not be empty!')
        if type(username) != str: raise TypeError('Name must be a string')
        if username == '' or username.isspace(): raise ValueError('Username must not be empty!')
        if len(username) > 24: raise ValueError('Username must not exceed 24 characters!')
        if len(username) < 5: raise ValueError('Username must not be less than 5 characters!')
        if type(password) != str: raise TypeError('Password must be a string')
        if password == '' or password.isspace(): raise ValueError('Password must not be empty!')
        if len(password) < 8: raise ValueError('Password must not be less than 8 characters!')

        
        self.email = email
        self.username = username
        self.password = password

    def __str__(self):
        return f"My name is {self.name}."
    
    @classmethod
    def from_document(cls, document):
        """Constructs and returns a new user from a JSON document"""
        return User(document['email'], document['username'], document['password'])
        
    def to_document(self):
        '''Hashes/salts password and returns the user instance in document/JSON format'''
        
        salt = bcrypt.gensalt()

        return {'email': self.email,
                'username': self.username,
                'password': bcrypt.hashpw(self.password.encode('utf-8'), salt),
                'cart': []}

    
    