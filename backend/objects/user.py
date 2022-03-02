class User:
    
    def __init__(self, name):
          self.name = name.lower().capitalize()

    def __str__(self) -> str:
        return f"My name is {self.name}."