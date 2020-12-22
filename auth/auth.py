from werkzeug.security import safe_str_cmp
from api.models import User
from database.db_manager import DbManager
import sys

DB = DbManager()

def authenticate(email, password):
    user = User(*DB.get_user(email))
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User(*DB.get_user_by_id(user_id))
