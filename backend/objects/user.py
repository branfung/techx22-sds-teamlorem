class User:
    
    def __init__(self, name):
          self.name = name.capitalize()

    def __str__(self):
        return f"My name is {self.name}."
    
print(User('BRANDON'))