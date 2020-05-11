from werkzeug.security import safe_str_cmp
from resources.user import User

def authenticate(username, password):
    # using sqlite database for retrieving user
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    # using sqlite database for retrieving user
    return User.find_by_id(user_id)
