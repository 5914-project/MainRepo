import pandas as pd

try:
    df_cate = pd.read_csv('./cate.csv')
except Exception:
    df_cate = pd.read_csv('./AI_Rec/cate.csv')
finally:
    pass

df_gby = df_cate.groupby('Category')

tmp = [x[0] for x in df_gby]
# print(df_gby)

labels_map = {x[0]: x[1] for x in enumerate(tmp)}
# {0: 'bread', 1: 'butter', 2: 'cheese', 3: 'milk', 4: 'apple', 5: 'banana', 6: 'bell pepper',
#           7: 'blackberry', 8: 'orange', 9: 'blueberry', 10: 'cherry', 11: 'coconut', 12: 'cucumber',
#           13: 'eggplant', 14: 'grape', 15: 'kiwi', 16: 'lemon', 17: 'lime', 18: 'lychee', 19: 'mango', 20: 'olive',
#           21: 'papaya', 22: 'passionfruit', 23: 'peach', 24: 'pear', 25: 'pineapple', 26: 'plum', 27: 'raspberry',
#           28: 'strawberry', 29: 'tomato', 30: 'watermelon', 31: 'potatoes', 32: 'yam', 33: 'pepper', 34: 'pumpkin',
#           35: 'kale', 36: 'mustard', 37: 'redbull', 38: 'coke', 39: 'tofu', 40: 'beef', 41: 'hams', 42: 'kebabs',
#           43: 'pork', 44: 'bacon', 45: 'egg', 46: 'rice', 47: 'fish', 48: 'shrimp', 49: 'lobster', 50: 'syrups',
#           51: 'chocolate', 52: 'dumpling', 53: 'noodle', 54: 'pasta', 55: 'pie', 56: 'salad', 57: 'sauce',
#           58: 'ketchup', 59: 'water', 60: 'sausage', 61: 'onion'}
labels_map_r = {x[1]: x[0] for x in enumerate(tmp)}
# {'bread': 0, 'butter': 1, 'cheese': 2, 'milk': 3, 'apple': 4, 'banana': 5, 'bell pepper': 6,
#             'blackberry': 7, 'orange': 8, 'blueberry': 9, 'cherry': 10, 'coconut': 11, 'cucumber': 12,
#             'eggplant': 13, 'grape': 14, 'kiwi': 15, 'lemon': 16, 'lime': 17, 'lychee': 18, 'mango': 19,
#             'olive': 20,
#             'papaya': 21, 'passionfruit': 22, 'peach': 23, 'pear': 24, 'pineapple': 25, 'plum': 26, 'raspberry': 27,
#             'strawberry': 28, 'tomato': 29, 'watermelon': 30, 'potatoes': 31, 'yam': 32, 'pepper': 33,
#             'pumpkin': 34,
#             'kale': 35, 'mustard': 36, 'redbull': 37, 'coke': 38, 'tofu': 39, 'beef': 40, 'hams': 41, 'kebabs': 42,
#             'pork': 43, 'bacon': 44, 'egg': 45, 'rice': 46, 'fish': 47, 'shrimp': 48, 'lobster': 49, 'syrups': 50,
#             'chocolate': 51, 'dumpling': 52, 'noodle': 53, 'pasta': 54, 'pie': 55, 'salad': 56, 'sauce': 57,
#             'ketchup': 58, 'water': 59, 'sausage': 60, 'onion': 61}
print(labels_map)
print(f"classes len: {labels_map.__len__()}")
