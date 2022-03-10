import unittest 
from objects.product import Product

# Data for Initial tests
testProductName = "Hoodie"
testProductPrice = 19.99
testProductQuantity = 3
testProductCreaterName = "S34L"

# Products Instances to test class methods
testProduct = Product(testProductName,testProductPrice,testProductCreaterName,testProductQuantity)
testTshirt = Product("T-Shirt", 4.99,"Bran",10)
testLongSleeve = Product("Long Sleeve", 9.99,"Y4N",1)

class TestProduct(unittest.TestCase):
    
    def test_argument_values(self):

        # Price has to be greater than 0 and less than or equal to 100
        self.assertRaises(ValueError,Product,testProductName, 149.99, testProductName,testProductQuantity)
        self.assertRaises(ValueError,Product,testProductName,-1,testProductName,testProductQuantity)
        self.assertRaises(ValueError,Product,testProductName,0,testProductName,testProductQuantity)
        self.assertRaises(ValueError,Product,testProductName,1000,testProductName,testProductQuantity)

        # Quantity has to be greater than 0 and less than or equal to 50
        self.assertRaises(ValueError,Product,testProductName,testProductPrice,testProductCreaterName,-1)
        self.assertRaises(ValueError,Product,testProductName,testProductPrice,testProductCreaterName,0)
        self.assertRaises(ValueError,Product,testProductName,testProductPrice,testProductCreaterName,70)
        self.assertRaises(ValueError,Product,testProductName,testProductPrice,testProductCreaterName,100)

    def test_argument_types(self):

        # Product Name and Product creator ID name must be a string
        self.assertRaises(TypeError,Product, 9230475, testProductPrice,testProductCreaterName,testProductQuantity)
        self.assertRaises(TypeError,Product, ["hello"], testProductPrice, testProductCreaterName,testProductQuantity)
        self.assertRaises(TypeError,Product, {"Hello":917}, testProductPrice,testProductCreaterName,testProductQuantity)
        self.assertRaises(TypeError,Product, ("hello","world"), testProductPrice,testProductCreaterName,testProductQuantity)
        self.assertRaises(TypeError,Product, 99.999, testProductPrice,testProductCreaterName,testProductQuantity)

        self.assertRaises(TypeError,Product,testProductName,testProductPrice,False,testProductQuantity)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,["Darth","Vader"],testProductQuantity)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,{"Anakin":"Darth","Skywalker":"Vader"},testProductQuantity)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,("Luke","Skywalker"),testProductQuantity)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,123,testProductQuantity)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,9.99,testProductQuantity)


        # product quantity must be integer
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,"Star Wars")
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,True)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,45.97)
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,[1,2,3,"hello"])
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,{"you":1,"are":2,"awesome":3})
        self.assertRaises(TypeError,Product,testProductName,testProductPrice,testProductQuantity,("General","Kenobi"))


        # product price must be int or float 
        self.assertRaises(TypeError,Product,testProductName,"Palpatine",testProductCreaterName,testProductQuantity)
        self.assertRaises(TypeError,Product,testProductName,["Emperor","Palpatine"],testProductCreaterName,testProductQuantity)
        self.assertRaises(TypeError,Product,testProductName,{"Emperor":"Palpatine","Darth":"Sidius"},testProductCreaterName,testProductQuantity)
        self.assertRaises(TypeError,Product,testProductName,("Darth","Bane"),testProductCreaterName,testProductQuantity)
        self.assertRaises(TypeError,Product,testProductName,False,testProductCreaterName,testProductQuantity)


    def test_update_price(self):

        # price must be a int or float
        self.assertRaises(TypeError,Product.update_price,self,"Harry")
        self.assertRaises(TypeError,Product.update_price,self,["Harry","Potter"])
        self.assertRaises(TypeError,Product.update_price,self,{"Harry":"Potter","Hermione":"Granger"})
        self.assertRaises(TypeError,Product.update_price,self,("Ron","Weasley"))

        # price must be less than or equal to 100
        self.assertRaises(ValueError,Product.update_price,self,-1)
        self.assertRaises(ValueError,Product.update_price,self,0)
        self.assertRaises(ValueError,Product.update_price,self,101)
        self.assertRaises(ValueError,Product.update_price,self,1394)

        
        testProduct.update_price(9.99)
        self.assertEqual(testProduct.price,9.99)

        testTshirt.update_price(5.99)
        self.assertEqual(testTshirt.price,5.99)

        testLongSleeve.update_price(15.57)
        self.assertEqual(testLongSleeve.price, 15.57)

    def test_update_quantity(self):

        # quantity must be a integer
        self.assertRaises(TypeError, Product.update_quantity,self,43.10)
        self.assertRaises(TypeError, Product.update_quantity,self,"Frodo")
        self.assertRaises(TypeError, Product.update_quantity,self,["Frodo","Gandalf"])
        self.assertRaises(TypeError, Product.update_quantity,self,{"Frodo":"Gandalf","Sauron":"Golum"})
        self.assertRaises(TypeError, Product.update_quantity,self,("Samwise","Legolas"))

        testProduct.update_quantity(2)
        self.assertAlmostEqual(testProduct.quantity,5)

        testTshirt.update_quantity(-5)
        self.assertEqual(testTshirt.quantity,5)

        testLongSleeve.update_quantity(10)
        self.assertEqual(testLongSleeve.quantity,11)


if __name__ == '__main__':
    unittest.main()



        



    
