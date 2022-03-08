from objects.order import Order

order1 = Order("Quebradillas", "Puerto Rico","Sebastian","Estrada", "sebastian.estrada@upr.edu", "787-718-7123","P.0.Box 1079", "00678")
print(order1)
print("Tracking ID: " + order1.getTrackingID())
