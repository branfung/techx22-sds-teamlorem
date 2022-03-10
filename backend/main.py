from objects.user import User
from objects.shop import Shop
from objects.product import Product


def main():
    store = Shop()

    print('Welcome to Populus Designs!')

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

    user = User(name)
    print(f'Hello, {user.name}! \n')
    
    open = True
    while open:
        print('Would you like to buy or sell a product? \n')
        option = input('Select an option [buy|sell|exit]: ').lower()
        

        if option == 'buy':
            keep_buying = True
            print('These are the products available at the moment')
            store.print_inventory()
            item = input('What is the id of the product you would like to buy? ')
            # Do we want add the items on a temp list and then create the order or create the order and with the shipping info blank and then have setters to update them ? 
            #TODO - Create an order
            
            #TODO - Ask the client if they want to buy another product 
            while keep_buying:
                decision = input('Would you like to buy another item? enter y for yes and n for no')
                if decision not in ['y', 'n']:
                    print('Something went wrong! Please make sure you typed either y or n.')
                elif decision == 'n':
                    keep_buying = False
                else:
                    # this brings a problem if we wait to update inventory after order is completed the user could add more items than the one we have on the store 
                    # should we update inventory as we go ? 
                    item = input('What is the id of the product you would like to buy?')


            #TODO - Remove all the products in the order from the store 
            #TODO - Add shipping and payment information
            print('Thank you for your purchase!')
            print('Hope to see you again soon and stay awesome!')

        elif option == 'sell':
            new_product = None
            
            print('Please provide the following information. \n')
            
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

            new_product = Product(product_name, product_price, user.name, product_quantity)               
                                    
            store.add_product(new_product)   
            print('The item has been successfully added.')

            store.print_inventory()
            print('Thank you for using Populus Designs to share your uniqueness with the world!')
            
            
        elif option == 'exit':
            open = False
            print('\n\nStay awesome, bye! :D')
            break
        else:
            print('Something went wrong! Please make sure you typed an option correctly when prompted! \n')

        


# def populate_store():
#     store.add_product(Product('Sloth Tee Shirt Medium',10,2))
#     store.add_product(Product("Mike's Bachelors Party Long Sleeve Large",12,1))
#     store.add_product(Product("Johson's Vacay Hoodie Extra Large",20,3))


if __name__ == '__main__':
    main()