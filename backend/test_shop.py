from asynchat import simple_producer
import unittest
from objects.product import Product
from objects.shop import Shop

class TestShop(unittest.TestCase):
    simple_product = Product('Simple Product', 1.00, 0, 'tester')
    more_than_one = Product('Multiple of the Same Product', 0.50, 1, 'tester', 45)
    another_product = Product('Another Simple Product', 1.00, 2, 'tester')
    existing_id_different_product = Product('Different Product', 2.00, 0, 'tester')
    
    shop1 = Shop()
    
    def test_shop_init(self):
        self.assertIsInstance(shop1, Shop)
    
    def test_shop_add_product(self):
        #test adding a product
        shop1.add_product(simple_product)
        self.assertEqual(shop1.inventory[simple_product.prodcut_id], simple_product)
            
        #test adding an existing product
        shop1.add_product(simple_product)
        self.assertEqual(shop1.inventory[simple_product.prodcut_id].quantity, 2)
        
        #test adding an existing product with quantity > 1
        simple_product.quantity = 5
        shop1.add_product(simple_product)
        self.assertEqual(shop1.inventory[simple_product.prodcut_id].quantity, 7)
        
        #test adding new product with quantity > 1
        shop1.add_product(more_than_one)
        shop1.add_product(more_than_one)
        self.assertEqual(shop1.inventory[more_than_one.product_id].quantity, 90)
        
        #test adding a different product with an already existing product_id
        self.assertRaises(ValueError, shop1.add_product(existing_id_different_product), 'Must not replace an existing product')
            
    def test_shop_remove_product(self):
        #test removing a product:
        simple_product.quantity = 7
        shop1.remove_product(simple_product)
        self.assertTrue(simple_product not in shop1.inventory)
        
        #test removing a product a product not in shop:
        self.assertRaises(ValueError, shop1.remove_product(another_product), 'Must only remove products that currently exist in the shop')
        
        #test removing more product than the current quantity:
        more_than_one.quantity = 200
        self.assertRaises(ValueError, shop1.remove_product(more_than_one), 'Must not remove more than the existing quantity')
        
if __name__ == '__main__':
    unittest.main()