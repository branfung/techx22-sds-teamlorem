from objects.shop import Shop
from objects.order import Order
from objects.product import Product
from objects.user import User
# used to validate email input 
import re
# used to open HTML file in browser
import webbrowser

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def main():

    # Instantiate the store! 
    store = Shop()
    populate_store(store) # add items !
    print('Welcome to Populus Designs!')

    # Validate input
    invalid_name = True
    while invalid_name:
        
        name = input('Enter a username (16 character limit): ')
        
        if name == '' or name.isspace():
            print('Name cannot be empty!')
        elif len(name) > 16:
            print('Character limit exceeded!')
        else:
            invalid_name = False
            break

    # Emulate a login
    user = User(name)
    print(f'Hello, {user.name}! \n')
    
    open = True
    while open:
        print('Would you like to buy or sell a product? \n')
        option = input('Select an option [buy|sell|exit]: ').lower()
        print()        

        if option == 'buy':

            keep_buying = True
            print('These are the products available at the moment \n')
            store.print_inventory()
            print()
            item = input('What is the id of the product you would like to buy? ')

            # get shipping info from the client to create an order
            while True:
                try:
                    
                    client_first_name = input("What is the name of the person for the order to be shipped at? ")
                    if not client_first_name.isalpha():
                        raise Exception

                    client_last_name = input("Whats is the last name of the person for the order to be shipped at? ")
                    if not client_last_name.isalpha():
                        raise Exception

                    client_email = input("Whats is the email of the person for the order to be shipped at? ")
                    if not re.fullmatch(regex,client_email):
                        raise Exception

                    client_phone_number = int(input("Whats is the phone number of the person for the order to be shipped at? "))
                    
                    client_street_address = input("Whats is the street address of the person for the order to be shipped at? ")
                   
                    client_city = input("Whats is the city of the person for the order to be shipped at? ")
                    
                    client_country = input("Whats is the country of the person for the order to be shipped at? ")
                    if not client_country.isalpha():
                        raise Exception

                    client_zip_code = int(input("Whats is the zip code of the person for the order to be shipped at? "))

                    client_phone_number = str(client_phone_number)
                    client_zip_code = str(client_zip_code)
   
                except:
                    print("Wrong inputs. Please try again. Remember to make sure your information is correct.")

                # everything is valid:
                else:
                    break

            client_order = Order(client_city,client_country,client_first_name,client_last_name,client_email,client_phone_number,client_street_address,client_zip_code)

            
            while keep_buying:
                decision = input('Would you like to buy another item? enter y for yes and n for no ')
                if decision not in ['y', 'n']:
                    print('Something went wrong! Please make sure you typed either y or n. ')
                elif decision == 'n':
                    keep_buying = False
                else:
                    item = input('What is the id of the product you would like to buy? ')

 
            print("Here is your order: " + client_order.__str__() + "\n")
            print("Your tracking ID is: " + client_order.getTrackingID())
            client_order.return_order_txt()
            print("A copy of your order has been sent to our servers for validation and processsing")
            print('Thank you for your purchase!')
            print('Hope to see you again soon and stay awesome!')


        elif option == 'sell':
            
            print('Please provide the following information. \n')
            
            # Validate all the necessary inputs
            invalid_product_name = True
            while invalid_product_name:
                
                product_name = input('Name of the product you would like to add (24 character limit): ')
                
                if product_name == '' or product_name.isspace():
                    print('The product name cannot be empty! Please try again!')
                elif len(product_name) > 24:
                    print('Character limit exceeded! Please try again!')
                else:
                    invalid_product_name = False
                    break
            
            invalid_price = True
            while invalid_price:
                
                try:
                    product_price = round(float(input('How much will the product cost? ($1-$100): $')), 2)
                except:
                    print('Price must be a valid amount in range of $1-$100. Please try again!')
                    
                if product_price <= 0 or product_price > 100:
                    print('Invalid input. Price must be a valid amount in range of $1-$100. Please try again!')
                else:
                    invalid_price = False
                    break
                    
            invalid_quantity = True
            while invalid_quantity:
                
                try:
                    product_quantity = int(input('How many would you like to add? (1-50): '))
                except:
                    print('Invalid input. Price must be a valid amount in range of 1-50. Please try again!')
                    
                if product_quantity <= 0 or product_quantity > 50:
                    print('Invalid input. Price must be a valid amount in range of 1-50. Please try again!')
                else:
                    invalid_quantity = False
                    break
            # End validation
            
            # Creates a new product to be added to the store
            new_product = Product(product_name, product_price, user.name, product_quantity)               
                                    
            store.add_product(new_product)   
            print('The item has been successfully added. \n')

            store.print_inventory()
            print('Thank you for using Populus Designs to share your uniqueness with the world! \n')
            
            
        elif option == 'exit':
            open = False
            print('\n\nStay awesome, bye! :D')
            break
        else:
            print('Something went wrong! Please make sure you typed an option correctly when prompted! \n')


def populate_store(store: Shop):
    """Fills the indicated store with a predetermined amount of products

    Args:
        store (Shop): The store to be populated with placeholder products
    """
    store.add_product(Product('Python is Cool!', 6.00, 'Brandon', 5))
    store.add_product(Product('OOP is OP!', 7.99, 'Sebastian', 20))
    store.add_product(Product('Future SWE B)', 9.99, 'Yan', 3))


if __name__ == '__main__':
    main()