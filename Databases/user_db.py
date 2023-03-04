import pymongo
from pymongo import MongoClient

def initialize():
    cluster = MongoClient('mongodb+srv://admin:xOAKtwZDIwshgLvX@smart-recipes.rfjjamv.mongodb.net/?retryWrites=true&w=majority')
    db = cluster.smart_recipes
    user_db = db.users

    return user_db 