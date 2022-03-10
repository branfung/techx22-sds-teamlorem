from collections import defaultdict
from objects.product import Product
class Shop:

    p_id = 0

    def __init__(self):

        '''
        inventory is a dictionary that in the case a key does not exist i give a value of 0 instead of an error
        '''

        self.inventory = defaultdict(int)
    
    def add_product(self,product,quantity_to_be_added = 1):

        '''
        product must be an object of type product
        If valid update the quantity in case the product was already in the inventory or
        Add it to the inventory otherwise 
        '''

        if not isinstance(product, Product):
            raise TypeError('Product must be an instance of the Product class.')

        elif type(quantity_to_be_added) != int:
            raise TypeError('The quantity to be added must be an integer.')

        elif quantity_to_be_added < 1:
            raise ValueError('The value must be an integer greater than 0.')

        elif product.product_id in self.inventory:
            self.inventory[product.product_id].update_quantity(quantity_to_be_added)

        else:
            product.product_id = self.p_id
            self.inventory[self.p_id] = product
            self.p_id += 1
    
    def remove_product(self,product,quantity_to_be_removed = 1):

        '''
        product must be an object of type product 
        If valid and the quantity available is more than one, remove one from quantity because it means we have more in stock
        Otherwise delete the item because we have run out of it at the moment
        '''

        if not isinstance(product, Product):
            raise TypeError('Product must be an instance of the Product class.')

        elif type(quantity_to_be_removed) != int:
            raise TypeError('The quantity to be removed must be an integer greater or equal to one and less than or equal to the current quantity of the product.')

        elif product.product_id not in self.inventory:
            raise ValueError('Must only remove products that currently exist in the shop.')

        elif quantity_to_be_removed < 1:
            raise ValueError('The quantity to be removed must be greater than 0.')

        elif quantity_to_be_removed < self.inventory[product.product_id].quantity:
            self.inventory[product.product_id].update_quantity(-quantity_to_be_removed)

        elif quantity_to_be_removed == self.inventory[product.product_id].quantity:
            del self.inventory[product.product_id]

        else:
            raise ValueError('You cannot remove more than what is avaiable.')

    def print_inventory(self):

        '''
        Prints all the products in the inventory as per the __str__ method from the product class 
        '''

        for id, product in self.inventory.items():
            print(f'id: {id} | {product}')
            print('==========================================================')
