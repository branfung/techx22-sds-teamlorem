class Product:
    """Creates a Product that can be added into a Shop. It contains all the necessary information for purchases.

    Args:
        name (str): The name of the product design
        price (float): The price of the product
        quantity (int): The desired amount to be sold 
        product_id (int): The special id of this product
        creator (str): The username of the creator of this product design
    """
    
    def __init__(self, name: str, price: float, quantity: int, product_id: int, creator: str):

        #TODO - input validation (TDD)
        self.name = name
        self.price = price
        self.quantity = quantity
        self.product_id = product_id
        self.creator = creator
    
    def __str__(self):
        return f'{self.name} | ${self.price} | {self.quantity} in stock | by {self.creator}'
    
    def update_price(self, price: float):
        """Updates the price of the indicated product.

        Args:
            price (float): The updated price amount
        
        Returns:
            void
        """
        
        #TODO - input validation (TDD)
        self.price = price
        
    def update_quantity(self, quantity: int):
        """Updates the quantity of the indicated product in stock by adding a desired amount. 
        If the quantity is negative it will indicate that a purchase has been made.

        Args:
            quantity (int): The quantity amount to be restocked or removed from stock. 
            
        Returns:
            void
        """
        
        #TODO - input validation (TDD)
        self.quantity += quantity
        
    
      