import unittest
from objects.product import Product
from objects.order import Order

product1 = Product('Sloth Shirt', 12.50, 0, 'Leon')
product2 = Product('Tech Ex Hoodie', 50.0, 1, 'Google')
test_products = {product1.product_id:product1, product2.product_id:product2}
test_first_name = 'Yan'
test_last_name = 'Aquino'
test_street_address = '5995 Silver Palm Drive'
test_zip_code = '34747'
test_country = 'United States'
test_phone_number = '787-932-0510'
test_email = 'yaquino@techexchange.in'
test_city = 'Kissimmee'
test_order = Order(test_city, test_country, test_first_name, test_last_name , test_email, test_phone_number, test_street_address, test_zip_code)
test_order.products = test_products

class TestOrder(unittest.TestCase):

    def test_argument_types(self):
        # city, country, first_name, last_name, email, phone_number, street_addres, and zip_code must be strings
        self.assertRaises(TypeError, Order, [], test_country, test_first_name, test_last_name , test_email, test_phone_number, test_street_address, test_zip_code)
        self.assertRaises(TypeError, Order, test_city, 0, test_first_name, test_last_name , test_email, test_phone_number, test_street_address, test_zip_code)
        self.assertRaises(TypeError, Order, test_city, test_country, False, test_last_name , test_email, test_phone_number, test_street_address, test_zip_code)
        self.assertRaises(TypeError, Order, test_city, test_country, test_first_name, {}, test_email, test_phone_number, test_street_address, test_zip_code)
        self.assertRaises(TypeError, Order, test_city, test_country, test_first_name, test_last_name , 0, test_phone_number, test_street_address, test_zip_code)
        self.assertRaises(TypeError, Order, test_city, test_country, test_first_name, test_last_name , test_email, True, test_street_address, test_zip_code)
        self.assertRaises(TypeError, Order, test_city, test_country, test_first_name, test_last_name , test_email, test_phone_number, 123, test_zip_code)
        self.assertRaises(TypeError, Order, test_city, test_country, test_first_name, test_last_name , test_email, test_phone_number, test_street_address, False)

    
    def test_update_order(self):
        # to_remove must be a boolean to_remove
        self.assertRaises(TypeError, Order.update_order, self, 'False', 0, test_products)

        # product_id must be an int
        self.assertRaises(TypeError, Order.update_order, self, False , '12345', test_products)

        # product_to_be_added must an instance of the Product class
        self.assertRaises(TypeError, Order.update_order, self, False , 1234567891234567, 0)

        # method succesfully removes the item from the order
        test_order.update_order(True, 0, None)
        self.assertEqual(test_order.products, {product2.product_id:product2})

        # method succesfully adds the item to the order 
        test_order.update_order(False, product1.product_id, product1)
        self.assertEqual(test_order.products, {product1.product_id:product1, product2.product_id:product2})

    def test_generate_tracking(self):
        # create a tracking ID for the order 
        test_order.generate_tracking()

        # tracking must be a string
        self.assertRaises(TypeError, test_order.getTrackingID, 1234567891234567)

        # assert that the tracking is correct length
        self.assertEqual(len(test_order.getTrackingID), 16)
        
    