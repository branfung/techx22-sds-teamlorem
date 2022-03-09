from objects.shop import Shop
from objects.order import Order
from objects.product import Product
from objects.user import User
store = Shop()


def main():
    #populate_store()
    print('Welcome to Populus Designs!')
    user_role = input('Would you like to buy or sell a product? Type "buy" or "sell" to make your choice ')
    while user_role.lower() not in ['buy', 'sell']:
        print('Something went wrong! Please make sure you typed either buy or sell when asked. ')
        user_role = input('Would you like to buy or sell a product? ')

    if user_role == 'buy':

        keep_buying = True
        print('These are the products available at the moment')
        store.print_inventory()
        item = input('What is the id of the product you would like to buy? ')

        # get shipping info from the client to create an order
        client_first_name = str(input("What is the name of the person for the order to be shipped at? "))
        client_last_name = str(input("Whats is the last name of the person for the order to be shipped at? "))
        client_email = str(input("Whats is the email of the person for the order to be shipped at? "))
        client_phone_number = str(input("Whats is the phone number of the person for the order to be shipped at? "))
        client_street_address = input(str("Whats is the street address of the person for the order to be shipped at? "))
        client_city = str(input("Whats is the city of the person for the order to be shipped at? "))
        client_country = str(input("Whats is the country of the person for the order to be shipped at? "))
        client_zip_code = str(input("Whats is the zip code of the person for the order to be shipped at? "))

        client_order = Order(client_city,client_country,client_first_name,client_last_name,client_email,client_phone_number,client_street_address,client_zip_code)

        
        #TODO - Ask the client if they want to buy another product 
        while keep_buying:
            decision = input('Would you like to buy another item? enter y for yes and n for no ')
            if decision not in ['y', 'n']:
                print('Something went wrong! Please make sure you typed either y or n. ')
            elif decision == 'n':
                keep_buying = False
            else:
                # this brings a problem if we wait to update inventory after order is completed the user could add more items than the one we have on the store 
                # should we update inventory as we go ? 
                item = input('What is the id of the product you would like to buy? ')


        #TODO - Remove all the products in the order from the store 
        print("Here is your order: " + client_order.__str__() + "\n")
        print("Your tracking ID is: " + client_order.getTrackingID())
        client_order.return_order_txt()
        print("A copy of your order has been sent to our servers for validation and processsing")
        print('Thank you for your purchase!')
        print('Hope to see you again soon and stay awesome!')

    else:
        product_name = input('Please enter the name of the product you would like to add: ')
        product_price = input('Please enter the cost of the product: ')
        product_quantity = input('What quantity of this particular product that you would like to add? ')
        #new_product = Product(product_name, product_price, product_quantity)
        #store.add_product(new_product)
        store.print_inventory()
        print('The item has been successfully added.')
        print('Thank you for using Populus Designs to share your uniqueness with the world!')
        print('Stay awesome, bye! :D')


# def populate_store():
#     store.add_product(Product('Sloth Tee Shirt Medium',10,2))
#     store.add_product(Product("Mike's Bachelors Party Long Sleeve Large",12,1))
#     store.add_product(Product("Johson's Vacay Hoodie Extra Large",20,3))


if __name__ == '__main__':
    main()