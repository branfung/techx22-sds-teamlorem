from collections import defaultdict
class Shop:

    def __init__(self):
        '''
        inventory is a dictionary that in the case a key does not exist i give a value of 0 instead of an error
        '''
        self.inventory = defaultdict(int)
    
    def add_product(self,product):
        '''
        product must be an object of type product
        If valid update the quantity in case the product was already in the inventory or
        Add it to the inventory otherwise 
        '''
        if self.inventory[product.product_id] == product:
            product.quantity += 1
        else:
            self.inventory[product.product_id] = product
    
    def remove_product(self,product):
        '''
        product must be an object of type product 
        If valid and the quantity available is more than one, remove one from quantity because it means we have more in stock
        Otherwise delete the item because we have run out of it at the moment
        '''
        if product not in self.inventory:
            raise ValueError('The product must be in the inventory in order to be removed')
        elif self.inventory[product.product_id].quantity > 1:
            self.inventory[product.product_id].quantity -= 1
        else:
            del self.inventory[product.product_id]

    def print_inventory(self):
        '''
        Prints all the products in the inventory as per the __str__ methof from the product class 
        '''
        for key in self.inventory:
            print(key.__str__())