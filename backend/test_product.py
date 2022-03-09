import unittest 
from objects.product import Product

# Data for Initial tests
testProductName = "Hoodie"
testProductPrice = 19.99
testProductQuantity = 3
testProductID = 9348664
testProductCreaterName = "S34L"

# Products Instances to test class methods
testProduct = Product(testProductName,testProductPrice, testProductQuantity, testProductID, testProductCreaterName)
testTshirt = Product("T-Shirt", 4.99, 2, 834546, "Bran")
testLongSleeve = Product("Long Sleeve", 9.99, 1, 13141, "Y4N")

class TestProduct(unittest.TestCase):
    
    # def setUp(self):
    #     try:
    #         self.tshirt_test = Product("T-Shirt",9.99,2,8374101,"S34L")
    #         self.long_sleeve_test = Product("Long Sleeve",15.99,2,5242358,"Bran")
    #         self.hoodie_test = Product("Hoodie",19.99,2,2575983,"Y7n")
    #         self.temp_product_test = Product("Shirt",4.99,2,6248725,"lorem")
    #     except:
    #         print("\n You must pass 5 parameters to create a Product instance.These parameters are: Name of the Product, Price, Quantity, Product ID and Creator name.")



    def test_arguments_values(self):

        # Price has to be greater than 0 and less than or equal to 100
        self.assertRaises(ValueError,Product,testProductName, 149.99, testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(ValueError,Product,testProductName,-1,testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(ValueError,Product,testProductName,0,testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(ValueError,Product,testProductName,1000,testProductQuantity,testProductID,testProductCreaterName)

        # Quantity has to be greater than 0 and less than or equal to 50
        self.assertRaises(ValueError,Product,testProductName,testProductPrice,-1,testProductID,testProductCreaterName)
        self.assertRaises(ValueError,Product,testProductName,testProductPrice,0,testProductID,testProductCreaterName)
        self.assertRaises(ValueError,Product,testProductName,testProductPrice,70,testProductID,testProductCreaterName)
        self.assertRaises(ValueError,Product,testProductName,testProductPrice,100,testProductID,testProductCreaterName)

    def test_argument_types(self):

        # Product Name and Product creator ID name must be a string
        self.assertRaises(TypeError,Product, 9230475, testProductPrice, testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product, ["hello"], testProductPrice, testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product, {"Hello":917}, testProductPrice, testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product, ("hello","world"), testProductPrice, testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product, 99.999, testProductPrice, testProductQuantity,testProductID,testProductCreaterName)

        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,testProductID,129412)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,testProductID,45.97)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,testProductID,[1,2,3,"hello"])
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,testProductID,{"you":1,"are":2,"awesome":3})
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,testProductID,("General","Kenobi"))

        # product quantity and ID must be integer
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,"Anakin",testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,["Darth","Vader"],testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,{"Anakin":"Darth","Skywalker":"Vader"},testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,("Luke","Skywalker"),testProductID,testProductCreaterName)

        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,"Leia",testProductCreaterName)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,["Leia","Organa"],testProductCreaterName)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,{"Leia":"Han","Organa":"Solo"},testProductCreaterName)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,("Ben","Solo"),testProductCreaterName)

        # product price must be int or float 
        self.assertRaises(TypeError,Product,testProductName,"Palpatine",testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product,testProductName,["Emperor","Palpatine"],testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product,testProductName,{"Emperor":"Palpatine","Darth":"Sidius"},testProductQuantity,testProductID,testProductCreaterName)
        self.assertRaises(TypeError,Product,testProductName,("Darth","Bane"),testProductQuantity,testProductID,testProductCreaterName)


    def test_update_price(self):

        # price must be a float
        self.assertRaises(TypeError,Product.update_price,self,90)
        self.assertRaises(TypeError,Product.update_price,self,"Harry")
        self.assertRaises(TypeError,Product.update_price,self,["Harry","Potter"])
        self.assertRaises(TypeError,Product.update_price,self,{"Harry":"Potter","Hermione":"Granger"})
        self.assertRaises(TypeError,Product.update_price,self,("Ron","Weasley"))

        # price must be greater than 0 and less than or equal to 100
        self.assertRaises(ValueError,Product.update_price,self,-1)
        self.assertRaises(ValueError,Product.update_price,self,0)
        self.assertRaises(ValueError,Product.update_price,self,101)
        self.assertRaises(ValueError,Product.update_price,self,1394)

        
        testProduct.update_price(9.99)
        self.assertEqual(testProduct.price,29.98)

        testTshirt.update_price(5.99)
        self.assertEqual(testTshirt.price,10.98)

        testLongSleeve.update_price(15.57)
        self.assertEqual(testLongSleeve.price, 25.56)

    def test_update_quantity(self):

        # quantity must be a integer
        self.assertRaises(TypeError, Product.update_quantity,self,43.10)
        self.assertRaises(TypeError, Product.update_quantity,self,"Frodo")
        self.assertRaises(TypeError, Product.update_quantity,self,["Frodo","Gandalf"])
        self.assertRaises(TypeError, Product.update_quantity,self,{"Frodo":"Gandalf","Sauron":"Golum"})
        self.assertRaises(TypeError, Product.update_quantity,self,("Samwise","Legolas"))

        testProduct.update_quantity(2)
        self.assertAlmostEqual(testProduct.quantity,5)

        testTshirt.update_quantity(5)
        self.assertEqual(testTshirt.quantity,7)

        testLongSleeve.update_price(10)
        self.assertEqual(testLongSleeve.quantity,11)



        



    
