import unittest
from objects.product import Product
from objects.Shop import Shop

simple_product = Product('Simple Product', 1.00, 'tester')
more_than_one = Product('Multiple of the Same Product', 0.50,'tester', 45)
another_product = Product('Another Simple Product', 1.00, 'tester')

shop1 = Shop()

class TestShop(unittest.TestCase):
    
    def test_shop_init(self):
        self.assertIsInstance(shop1, Shop)
    
    def test_shop_add_product(self):
        # Test if what we are adding is a product 
        self.assertRaises(TypeError, shop1.add_product, True)

        # Test adding a product
        shop1.add_product(simple_product)
        self.assertEqual(shop1.inventory[simple_product.product_id], simple_product)
            
        # Test adding an existing product
        shop1.add_product(simple_product)
        self.assertEqual(shop1.inventory[simple_product.product_id].quantity, 2)
        
        # Updating the quantity of an existing product with quantity > 1
        shop1.add_product(simple_product, 5)
        self.assertEqual(shop1.inventory[simple_product.product_id].quantity, 7)
        
        # Test adding new product with quantity > 1
        shop1.add_product(more_than_one)
        self.assertEqual(shop1.inventory[more_than_one.product_id].quantity, 45)
                    
    def test_shop_remove_product(self):

        # Testing the type of product 
        self.assertRaises(TypeError, shop1.remove_product, True, 1)

        # Testing the type of quantity_to_be_removed
        self.assertRaises(TypeError, shop1.remove_product, simple_product, [])

        # Testing the value of quantity_to_be_removed
        self.assertRaises(ValueError, shop1.remove_product, simple_product, -17)

        # Testing removing a product: 
        shop1.remove_product(simple_product, simple_product.quantity)
        self.assertTrue(simple_product not in shop1.inventory)
        
        # Testing removing a product a product not in shop:
        
        self.assertRaises(ValueError, shop1.remove_product, another_product, 1)
        
        # Testing removing more product than the current quantity:

        self.assertRaises(ValueError, shop1.remove_product, more_than_one, 200)
        
if __name__ == '__main__':
    unittest.main()