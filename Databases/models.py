from flask import Flask, session

class User:

    def start_session(self, data):
        session['logged_in'] = True
        session['username'] = data['username']
        session['ingredients'] = data['ingredients']
        session['allergies'] = data['allergies']
        session['liked'] = data['liked']

    def signout(self):
        session.clear()

    def username(self):
        return session['username']
    
    def get_ingredients(self):
        return session['ingredients']
    
    def get_allergies(self):
        return session['allergies']
    
    def get_liked(self):
        return session['liked']

    def add_allergy(self, allergy):
        session['allergies'].append(allergy)
        session.modified = True

    def remove_allergy(self, allergy):
        session['allergies'].remove(allergy)
        session.modified = True

    def add_ingredient(self, ingredient):
        session['ingredients'].append(ingredient)
        session.modified = True

    def remove_ingredient(self, ingredient):
        session['ingredients'].remove(ingredient)
        session.modified = True

    def clear_ingredients(self):
        session['ingredients'].clear()
        session.modified = True

    def add_liked(self, id):
        session['liked'].append(id)
        session.modified = True

    def remove_liked(self, id):
        session['liked'].remove(id)
        session.modified = True