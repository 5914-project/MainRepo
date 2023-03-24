class User:

    def __init__(self, data):
        self.username = data['username']
        self.ingredients = data['ingredients']
        self.allergies = data['allergies']

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def add_allergy(self, allergy):
        self.allergies.append(allergy)

    def remove_ingredient(self, ingredient):
        self.ingredients.remove(ingredient)

    def clear_ingredients(self):
        self.ingredients.clear()

    def remove_allergy(self, allergy):
        self.allergy.remove(allergy)

    def get_ingredients(self):
        return self.ingredients
    
    def get_allergies(self):
        return self.allergies