
from encodings import utf_8
import os
import string
import random
import secrets
from typing import Type
from objects.product import Product


class Order:

    """ Class that represents a order instance. An order contains the shipping info of an client
    and the shoppingCart the user/client bought to be delivered to the built address with the provided
    information by the user/client

    Member Variables:
        city -> Member Variable that indicates the city of the order to be delivered
        country -> Member Variable that indicates the country of the order to be delivered
        email -> Member variable that indicates the client's email to send updates abour the shipping information
        first_name -> Member variable that represents the name of the person the order is destined to
        last_name ->  Member variable that represents the last name of the person the order is destined to 
        phone_number -> Member variable that represents the client's phone number
        shoppingCart ->  Member dictionary that holds all the items the client bought 
        street_address ->  Member variable that represents the street address for the order to be delivered 
        zip_code -> Member variable that represents the zip code for the order to be delivered
        tracking_ID -> Member variable that represents a unique tracking ID for the order

    Methods:
        __str__ -> method that represents the "print order" method, it returns the order as a string
        generate_tracking -> method that generates a unique tracking/shipping ID for the order 
        change_order -> method that allows the client to add/remove an product from the shopping cart (shoppingCart dict)

        class getters:
            methods that return the current value of a private member variable

        class setters:
            methods that change the value of the specified member variable

    """

    
    def __init__(self, city:str, country:str,first_name:str,last_name:str, email:str, phone_number:str, street_address:str, zip_code:str) -> None:

        """ Inits a Order with passed parameter and it creates unique tracking ID and shopping cart for the customer

        Raises:
            TypeError: If any of the parameters is not a string, the raise is executed
        """
        
        if type(city) is not str:
            raise TypeError("City must be a string. Please try again.")

        if type(country) is not str:
            raise TypeError("Country must be a string. Please try again.")

        if type(first_name) is not str:
            raise TypeError("First Name has to be a string.")

        if type(last_name) is not str:
            raise TypeError("Last Name has to be a string.")
        
        if type(email) is not str:
            raise TypeError("Email has to be a string.")

        if type(phone_number) is not str:
            raise TypeError("Phone number has to me written as a string.")
        
        if type(street_address) is not str:
            raise TypeError("Street Address must be a string.")

        if type(zip_code) is not str:
            raise TypeError("Zip Code has to be written as a string")
    
        self.city = city
        self.country = country
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.shoppingCart = {}
        self.street_address = street_address
        self.tracking_ID = self.generate_tracking()
        self.zip_code = zip_code

    # Print Order Method             
    def __str__(self) -> str:
        """ Creates a String representation of the class

        Returns:
            str: a string representing the class instance values. Notice that the phone number 
            output has been formatted to automatically output the value in the ###-###-### format
        """
        result = "First Name: " + self.first_name + "\n" + "Last Name: " + self.last_name + "\n" + "Country: " + self.getCountry() + "\n" + "City: " + self.city + "\n" + "Zip Code: " + self.zip_code + "\n" + "Street Address: " + self.street_address + "\n" + "Phone Number: " + "{}-{}-{}".format(self.phone_number[:3],self.phone_number[3:6], self.phone_number[6:]) + "\n" + "Your order contains the following products: " + "\n" 
        for product in self.shoppingCart.values():
            result += (str(product) + "\n")

        return result

    # Generate Tracking ID for each member 
    def generate_tracking(self) -> str:
        """ Generates a unique Tracking ID for this instance
        see reference: https://www.javatpoint.com/python-program-to-generate-a-random-string

        Returns:
            str: string representing a tracking ID of the order 
        """
        return "".join(secrets.choice(string.ascii_uppercase + string.digits) for x in range(16))
        
     
    # add/remove an product
    def update_order(self,to_remove:bool,product_id:int,product_to_be_added:Product) -> None:
        """ Update the shopping cart by removing or adding a product into it

        Args:
            to_remove (Boolean): Boolean value that indicates if the method is going to
            remove (True) or add (False)
            product_id (_type_): ID of the product to be added or removed into the shopping cart
            product_to_be_added (_type_): If it is a new product, this will be the product instance
            to be added into the shopping cart 

        Raises:
            TypeError: Product ID must be an integer in order to work
            TypeError: Product to be added must be a Product instance 
        """

        # if the option is to remove, check that a valid key has been passed in order to remove the product
        if type(product_id) is not int:
            raise TypeError("Product ID must be valid. Has to be an integer.") 

        if to_remove and product_id in self.shoppingCart.keys():
            self.shoppingCart.pop(product_id)
        
        # remove the indicated product from the dictionary
        if product_to_be_added is not None:
            if not isinstance(product_to_be_added,Product):
                raise TypeError("Product to be Added has to be an instance of the Product class")
            else:
                self.shoppingCart[product_id] = product_to_be_added

    def return_order_txt(self,order_total) -> None:
        """ Create a text file that represents the order instance information that has been created
        """
        if type(order_total) is not str:
            raise TypeError("Total must be passed as a string.")

        with open(self.first_name + self.last_name + "Order" +".txt","w", encoding="utf_8") as order_information:
            # os.makedirs('orders', exist_ok=True)
            order_information.write(self.__str__() + "\n")
            order_information.write("Your total is:$" + order_total + "\n")
            order_information.write("Thanks for ordering!")


    # Class Getters
    def getCity(self) -> str: return self.city
    def getCountry(self) -> str: return self.country
    def getEmail(self) -> str: return self.email
    def getFirstName(self) -> str: return self.first_name
    def getLastName(self) -> str: return self.last_name
    def getPhoneNumber(self) -> str: return self.phone_number
    def getshoppingCart(self) -> dict: return self.shoppingCart
    def getStreetAddress(self) -> str: return self.street_address
    def getTrackingID(self) -> str: return self.tracking_ID
    def getZipCode(self) -> str: return self.zip_code

    # Class Setters
    def setCity(self, new_city:str) -> None: self.city = new_city
    def setCountry(self,new_country:str) -> None: self.country = new_country
    def setEmail(self, new_email:str) -> None: self.email = new_email
    def setFirstName(self, new_first_name:str) -> None: self.first_name = new_first_name
    def setLastName(self,new_last_name:str) -> None: self.last_name = new_last_name
    def setPhoneNumber(self,new_phone_number:str) -> None: self.phone_number = new_phone_number
    def setshoppingCart(self,new_shoppingCart:str) -> None: self.shoppingCart = new_shoppingCart
    def setStreetAddress(self,new_street_address:str) -> None: self.street_address = new_street_address
    def setTrackingID(self,new_tracking_ID:str) -> None: self.tracking_ID = new_tracking_ID
    def setZipCode(self,new_zip_code:str) -> None: self.zip_code = new_zip_code


    #TODO

    # Edit update order method so that is more efficient (uses parametors more efficiently)
    # make member variables to be private 
    # print shopping cart items in the string and return order methods 



        
