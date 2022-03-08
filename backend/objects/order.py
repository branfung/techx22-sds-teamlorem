import string
import random
import secrets


class Order:

    """ Class that represents a order instance. An order contains the shipping info of an client
    and the products the user/client bought to be delivered to the built address with the provided
    information by the user/client

    Member Variables:
        city -> Private Member Variable that indicates the city of the order to be delivered
        country -> Private Member Variable that indicates the country of the order to be delivered
        email -> Private Member variable that indicates the client's email to send updates abour the shipping information
        existing_tracking_IDs -> Set Member variable that holds all the created tracking IDs through time. This is to make sure an ID is never repeated.
        first_name -> Private Member variable that represents the name of the person the order is destined to
        last_name -> Private Member variable that represents the last name of the person the order is destined to 
        phone_number -> Private Member variable that represents the client's phone number
        products -> Private Member dictionary that holds all the items the client bought 
        street_address -> Private Member variable that represents the street address for the order to be delivered 
        zip_code -> Private Member variable that represents the zip code for the order to be delivered
        tracking_ID -> Private Member variable that represents a unique tracking ID for the order

    Methods:
        __str__ -> method that represents the "print order" method, it returns the order as a string
        generate_tracking -> method that generates a unique tracking/shipping ID for the order 
        change_order -> method that allows the client to add/remove an product from the shopping cart (products dict)

        class getters:
            methods that return the current value of a private member variable

        class setters:
            methods that change the value of the specified member variable

    """

    
    def __init__(self, city, country,first_name,last_name, email, phone_number, street_address, zip_code) -> None:
        # private member variables 
        self.city = city
        self.country = country
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.products = {}
        self.street_address = street_address
        self.tracking_ID = self.generate_tracking()
        self.zip_code = zip_code

    # Print Order Method             
    def __str__(self) -> str:
        return "First Name: " + self.first_name + "\n" + "Last Name: " + self.last_name + "\n" + "Country: " + self.getCountry() + "\n" + "City: " + self.city + "\n" + "Zip Code: " + self.zip_code + "\n" + "Street Address: " + self.street_address + "\n" + "Phone Number: " + self.phone_number + "\n" + str(list(self.products.values()))

    # Generate Tracking ID for each member 
    def generate_tracking(self) -> str:
        return "".join(secrets.choice(string.ascii_uppercase + string.digits) for x in range(16))
        
     
    # add/remove an product
    def update_order(self,to_remove,product_id,product_to_be_added) -> None:
        # if True, remove the indicated product from the dictionary
        if to_remove:
            self.products.pop(product_id)
        else:
            self.products[product_id] = product_to_be_added

    # Class Getters
    def getCity(self) -> str: return self.city
    def getCountry(self) -> str: return self.country
    def getEmail(self) -> str: return self.email
    def getFirstName(self) -> str: return self.first_name
    def getLastName(self) -> str: return self.last_name
    def getPhoneNumber(self) -> str: return self.phone_number
    def getProducts(self) -> dict: return self.products
    def getStreetAddress(self) -> str: return self.street_address
    def getTrackingID(self) -> str: return self.tracking_ID
    def getZipCode(self) -> str: return self.zip_code

    # Class Setters
    def setCity(self, new_city) -> None: self.city = new_city
    def setCountry(self,new_country) -> None: self.country = new_country
    def setEmail(self, new_email) -> None: self.email = new_email
    def setFirstName(self, new_first_name) -> None: self.first_name = new_first_name
    def setLastName(self,new_last_name) -> None: self.last_name = new_last_name
    def setPhoneNumber(self,new_phone_number) -> None: self.phone_number = new_phone_number
    def setProducts(self,new_products) -> None: self.products = new_products
    def setStreetAddress(self,new_street_address) -> None: self.street_address = new_street_address
    def setTrackingID(self,new_tracking_ID) -> None: self.tracking_ID = new_tracking_ID
    def setZipCode(self,new_zip_code) -> None: self.zip_code = new_zip_code



        
