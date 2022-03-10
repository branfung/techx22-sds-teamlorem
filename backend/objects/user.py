class User:
    
    def __init__(self, name: str):
        """Creates a user that can be used to emulate a session.

        Args:
            name (str): The username of the current user
        """
        if type(name) != str: raise TypeError('Name must be a string')
        if name == '' or name.isspace(): raise ValueError('Name must not be empty!')
        if len(name) > 16: raise ValueError('Name must not exceed 16 characters!')
        
        self.name = name.capitalize()

    def __str__(self):
        return f"My name is {self.name}."
