items = []

def addItem(new_item):
    if new_item not in items:
        items.append(new_item)

def removeItems():
    items.clear()

def returnItems():
    return items