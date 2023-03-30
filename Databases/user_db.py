import pymongo, os, bcrypt
from pymongo import MongoClient
from Databases.models import User

DB = None

def initialize():
    global DB

    #cluster = MongoClient(os.environ.get('MONGODB'))
    cluster = MongoClient('mongodb+srv://admin:xOAKtwZDIwshgLvX@smart-recipes.rfjjamv.mongodb.net/?retryWrites=true&w=majority')
    db = cluster.smart_recipes
    user_db = db.users

    DB = user_db 

def login(username, password):
    user = DB.find_one({'username': username})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return None, user
    
    return 'Incorrect username or password.', None

def signup(username, password):
    if not DB.find_one({'username': username}):
        if len(username) == 0 or len(password) == 0:
            return 'Username or password cannot be empty.'
        
        DB.insert_one({
            'username': username, 
            'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()), 
            'ingredients':[], 
            'allergies':[]})
        
        return None, DB.find_one({'username': username})
    
    return 'Username already taken.', None

def update_doc(username):
    DB.update_one({'username': username},
                  {'$set': {
                            'ingredients': User().get_ingredients(),
                            'allergies': User().get_allergies(),
                            'username': User().username()
                            }
                    })