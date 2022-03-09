import unittest 
from objects.product import Product

class TestProduct(unittest.TestCase):
    
    def setUp(self):
        try:
            self.product1 = Product("T-Shirt",9.99,2,8374101,"S34L")
            self.product2 = Product("Long Sleeve",15.99,2,5242358,"Bran")
            self.product3 = Product("Hoodie",19.99,2,2575983,"Y7n")
            self.product4 = Product("Shirt",4.99,2,6248725,"lorem")
        except:
            print("\n You must pass 5 parameters to create a Product instance.These parameters are: Name of the Product, Price, Quantity, Product ID and Creator name.")

        

    def test_temp1(self):
        self.assertAlmostEqual()
        self.assertAlmostEqual()
        self.assertAlmostEqual()
        self.assertAlmostEqual()
        self.assertAlmostEqual()
        self.assertAlmostEqual()
        self.assertAlmostEqual()

    def test_temp2(self):
        self.assertRaises(ValueError)
        self.assertRaises(ValueError)
        self.assertRaises(ValueError)
        self.assertRaises(ValueError)
        self.assertRaises(TypeError)
        self.assertRaises(TypeError)
        self.assertRaises(TypeError)
        self.assertRaises(TypeError)

        
    def test_temp3(self):
        pass

    def test_temp(self):
        pass
