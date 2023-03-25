from flask import Flask, session

class User:

    def start_session(self, data):
        session['logged_in'] = True
        session['username'] = data['username']
        session['ingredients'] = data['ingredients']
        session['allergies'] = data['allergies']

    def signout(self):
        session.clear()

    def username(self):
        return session['username']

    def add_ingredient(self, ingredient):
        session['ingredients'].append(ingredient)
        session.modified = True

    def add_allergy(self, allergy):
        session['allergies'].append(allergy)
        session.modified = True

    def remove_ingredient(self, ingredient):
        session['ingredients'].remove(ingredient)
        session.modified = True

    def clear_ingredients(self):
        session['ingredients'].clear()

    def remove_allergy(self, allergy):
        session['allergies'].remove(allergy)
        session.modified = True

    def get_ingredients(self):
        return session['ingredients']
    
    def get_allergies(self):
        return session['allergies']