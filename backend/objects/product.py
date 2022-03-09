class Product:
    """Creates a Product that can be added into a Shop. It contains all the necessary information for purchases.

    Args:
        name (str): The name of the product design
        price (float): The price of the product
        product_id (int): The special id of this product
        creator (str): The username of the creator of this product design
        quantity (int): The desired amount to be sold. Defaults to 1.

    """
    
    def __init__(self, name: str, price: float, creator: str, quantity: int = 1):

        #TODO: input validation (TDD)
        self.name = name
        self.price = price
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
        
        #TODO: input validation (TDD)
        self.price = price
        return self
        
    def update_quantity(self, quantity: int):
        """Updates the quantity of the indicated product in stock by adding a desired amount. 
        If the quantity is negative it will indicate that a purchase has been made.

        Args:
            quantity (int): The quantity amount to be restocked or removed from stock. 
            
        Returns:
            self (Product obj)
        """
        
        #TODO: input validation (TDD)
        self.quantity += quantity
        return self
        
    
      