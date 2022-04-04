import requests
from model.objects.product import Product

def make_product(document, message={}):
    '''Validates and returns a Product object from a dictionary'''

    # Fetching the image_url from the user to check if it gives us headers        
    try:
        url = document['image_url']
        response = requests.get(url)
    except:
        # Handle error
        message['error'] = 'Something went wrong with your image URL'
    
    # Validating image_url to see if it's an image
    if response.headers.get('content-type') not in ['image/png', 'image/jpeg']:
        message['error'] = 'URL is not a valid image URL! Please use a correct URL'
    else:
        product = Product.from_document(document)
        return product