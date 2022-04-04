from model.objects.user import User

def make_user(document):
    '''Returns a User object from a dictionary/document'''

    user = User.from_document(document)
    return user