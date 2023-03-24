import pymongo, os
from pymongo import MongoClient

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

    if user and password == user['password']:
        return None, user
    
    return 'Incorrect username or password.', None

def signup(username, password):
    if not DB.find_one({'username': username}):
        if len(username) == 0 or len(password) == 0:
            return 'Username or password cannot be empty.'
        
        DB.insert_one({
            'username': username, 
            'password': password, 
            'ingredients':[], 
            'allergies':[]})
        
        return None, DB.find_one({'username': username})
    
    return 'Username already taken.', None

def update_doc(user, username):
    DB.update_one({'username': username},
                  {'$set': {
                            'ingredients': user.get_ingredients(),
                            'allergies': user.get_allergies(),
                            'username': user.username
                            }
                    })