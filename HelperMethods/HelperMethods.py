arr = {'coffee', 'milk', 'cheese', 'eggs', 'butter'}

#Returns keyword for food item from long string
def get_keyword(barcode):
    str = barcode[0].lower()
    for word in str.split():
        if word in arr:
            return word
    return None
