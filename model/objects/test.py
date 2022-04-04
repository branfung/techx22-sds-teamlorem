from product import Product
from shop import Shop

store = Shop()
# store.print_inventory()
product = Product('Dragon Force ffff Hoodie', 5.00, 'branfung')
print(len(product.name))
# print(product)
store.add_product(product)
# store.print_inventory()
product2 = Product('Grey TShirt', 10.00, 'YAN', 35)
store.add_product(product2)
store.print_inventory()

print(float('-2'))