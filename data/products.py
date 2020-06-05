import json


class Products:

    def __init__(self):
        self.path = 'products.json'

    def get_product(self, category, subcategory, id):
        with open(self.path, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)
        return data['Kategoria'][category][subcategory][id]
