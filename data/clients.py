import json


class Clients:

    def __init__(self):
        self.path = 'clients.json'

    def get_client(self, type_):
        with open(self.path, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)
        return data[type_]
