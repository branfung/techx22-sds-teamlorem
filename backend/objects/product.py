from typing import Type


class Product:
    """Creates a Product that can be added into a Shop. It contains all the necessary information for purchases.

    Args:
        name (str): The name of the product design
        price (int or float): The price of the product
        product_id (int): The special id of this product
        creator (str): The username of the creator of this product design
        quantity (int): The desired amount to be sold. Defaults to 1.

    """
    
    def __init__(self, name: str, price, creator: str, quantity: int = 1):

        if type(name) != str: raise TypeError('Name of this product must be a sting')
        if type(price) not in {float, int}: raise TypeError('Price must be an int or float!')
        if type(creator) != str: raise TypeError('Creator username must be a string!')
        if type(quantity) != int: raise TypeError('Quantity must be an integer!')
        
        if name == '' or name.isspace(): raise ValueError('Name must not be empty!')
        if len(name) > 24: raise ValueError('Name must not exceed 24 characters!')
        if price <= 0 or price > 100: raise ValueError('Price must be inside the $1-$100 range!')
        if creator == '' or creator.isspace(): raise ValueError('Creator username must not be empty!')
        if len(creator) > 16: raise ValueError('Creator username must not exceed 24 characters!')
        if quantity <= 0 or quantity > 50: raise ValueError('Quantity must be inside the 1-50 range!')
        
        self.name = name
        self.price = float(price)
        self.product_id = None
        self.creator = creator
        self.quantity = quantity

    
    def __str__(self):
        return f'{self.name} | ${self.price} | {self.quantity} in stock | by {self.creator}'
    
    def update_price(self, price: float):
        """Updates the price of the indicated product.

        Args:
            price (float): The updated price amount
        
        Returns:
            self (Product obj)
        """
        
        if type(price) not in {float, int}: raise TypeError('Price must be a valid number!')
        if price <= 0 or price > 100: raise ValueError('Price must be inside the $1-$100 range!')
        
        self.price = float(price)
        return self
        
    def update_quantity(self, quantity: int):
        """Updates the quantity of the indicated product in stock by adding a desired amount. 
        If the quantity is negative it will indicate that a purchase has been made.

        Args:
            quantity (int): The quantity amount to be restocked or removed from stock. 
            
        Returns:
            self (Product obj)
        """
        
        if type(quantity) != int: raise TypeError('Quantity must be an integer!')
        if self.quantity + quantity <= 0: raise ValueError('Cannot remove more than the existing amount!')
        if self.quantity + quantity > 50:
            exceeded = self.quantity + quantity - 50
            raise ValueError(f'Total quantity exceeded by {exceeded}')
        
        self.quantity += quantity
        return self
        
    
      