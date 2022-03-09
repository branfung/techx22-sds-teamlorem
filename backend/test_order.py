import unittest
# TODO - Import product class in order to to create product object to populate test_products
# TODO - Import Order Class in order to create an order 
#from objects.Product import Product

test_products = None
test_street_address = '5995 Silver Palm Drive'
test_zip_code = '34747'
test_state = 'Florida'
test_phone_number = '787-932-0510'
test_email = 'yaquino@techexchange.in'
test_city = 'Kissimmee'


class TestOrder(unittest.TestCase):

    def test_argument_types(self):

        # products must be a dictionary ? Like in inventory  
        self.assertRaises(TypeError, Order, [], test_street_address, test_zip_code, test_state, test_phone_number, test_email, test_city)

        # street_address, zip_code, state, phone_number, email, and city must be strings
        self.assertRaises(TypeError, Order, test_products, 0, test_zip_code, test_state, test_phone_number, test_email, test_city)
        self.assertRaises(TypeError, Order, test_products, test_street_address, False, test_state, test_phone_number, test_email, test_city)
        self.assertRaises(TypeError, Order, test_products, test_street_address, test_zip_code, [], test_phone_number, test_email, test_city)
        self.assertRaises(TypeError, Order, test_products, test_street_address, test_zip_code, test_state, {}, test_email, test_city)
        self.assertRaises(TypeError, Order, test_products, test_street_address, test_zip_code, test_state, test_phone_number, 0, test_city)
        self.assertRaises(TypeError, Order, test_products, test_street_address, test_zip_code, test_state, test_phone_number, test_email, True)
    
    def test_update_order(self):
        # to_remove must be a boolean to_remove
        self.assertRaises(TypeError, Order.update_order, self, 'False', 0, test_products)

        # product_id must be an int
        self.assertRaises(TypeError, Order.update_order, self, False , '12345', test_products)

        # product_to_be_added must an instance of the Product class
        self.assertRaises(TypeError, Order.update_order, self, False , 1234567891234567, 0)

        # method succesfully remove the item from the order
        test_order = Order()
        test_order.update_order(test_products[0])
        self.assertEquals(test_order.products, {})

        # method succesfully adds the item to the order 
        test_order2 = Order()
        test_order2.update_order(test_products[0])
        self.assertEquals(test_order2.products, {})

    def test_tracking(self):
        # tracking must be a string
        self.assertRaises(TypeError, Order.tracking , 1234567891234567)
        # assert that the tracking is correct length
        self.assertEqual(len(Order.tracking), 16)
        
    