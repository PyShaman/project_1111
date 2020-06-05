import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import data.clients as clients
import data.products as products


class GenerateBill:

    def __init__(self):
        self.client = clients.Clients()
        self.product = products.Products()

    def add_item_to_bill(self, category, subcategory, id_, quantity):
        product = self.product.get_product(category, subcategory, id_)
        return product['nazwa'], product['cena'], product['jednostka'], product['VAT'], product['PTU'], quantity

    def add_client_to_bill(self, type_, name):
        client = self.client.get_client(type_)
        for data in client:
            if data['nazwa'] == name:
                return data['adres']
