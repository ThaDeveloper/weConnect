import uuid


class User(object):
    """Store user data in dictionaries"""

    def __init__(self):
        self.users = {}
        self.u_token = {}

    def create_user(self, username, password, admin=False):
        """Creates a new user an append to the list of users"""
        data = {'id': uuid.uuid4(), 'username': username, 'password': password, 'admin': admin}
        self.users[username] = data
        return self.users


class Business(object):
    """Store business data in dictionaries"""

    def __init__(self):
        self.businesses = {}

    def register_business(self, name, description, location, category, user_id):
        """Adds a new  to businesses dictionary"""
        new_business = {'business_id': uuid.uuid4(), 'name': name, 'description': description, 'location': location,
                        'category': category, 'user_id': user_id}
        self.businesses[name] = new_business
        return self.businesses

    def find_business_by_id(self,business_id):
        for business in self.businesses:
            if self.businesses['business_id'] == business_id:
                return business