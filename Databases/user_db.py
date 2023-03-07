import pymongo
from pymongo import MongoClient

DB = None

def initialize():
    global DB

    cluster = MongoClient('mongodb+srv://admin:xOAKtwZDIwshgLvX@smart-recipes.rfjjamv.mongodb.net/?retryWrites=true&w=majority')
    db = cluster.smart_recipes
    user_db = db.users

    DB = user_db 

def login(username, password):
    user = DB.find_one({'username': username})

    if user and password == user['password']:
        return None
    
    return 'Incorrect username or password.'

def signup(username, password):
    if not DB.find_one({'username': username}):
        if len(username) == 0 or len(password) == 0:
            return 'Username or password cannot be empty.'
        
        DB.insert_one({'username': username, 'password': password, 'ingredients':[], 'allergies':[]})
        return None
    
    return 'Username already taken.'