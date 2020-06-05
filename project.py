import csv
import time
import uuid
from datetime import datetime, timedelta
from reports.bill import GenerateBill
from data.sort import Sorting
from data.clients import Clients


class Project:
    def __init__(self):
        self.current_date = datetime.today().strftime('%Y-%m-%d')
        self.current_time = time.strftime("%H:%M:%S", time.localtime())
        self.bill_number = str(uuid.uuid1())
        self.timestamp = str(datetime.now().isoformat()).replace(":", "-")[:10]
        self.bill = GenerateBill()
        self.sort = Sorting()

    @staticmethod
    def read_order(order_file):
        with open(order_file, newline = '') as csvfile:
            reader = csv.DictReader(csvfile, delimiter = ';')
            for row in reader:
                return row['Type'], row['Client']

    def generate_list_from_order(self, order_file):
        temp_list = []
        order_list = []
        with open(order_file, newline = '') as csvfile:
            reader = csv.DictReader(csvfile, delimiter = ';')
            for row in reader:
                temp_list.append(row)
            for element in temp_list:
                order_list.append(self.bill.add_item_to_bill(element['Category'], element['Subcategory'],
                                                             int(element['id']), int(element['quantity'])))
            return order_list

    def generate_bill(self, order_file):
        with open('example_bill.txt') as f:
            with open(f"output_bill_{self.timestamp}.txt", "w", encoding = 'utf-8') as f1:
                overall_net = []
                overall_gross = []
                bill_list = self.generate_list_from_order(order_file)
                for net in bill_list:
                    overall_net.append(net[1] * net[5])
                for gro in bill_list:
                    overall_gross.append((gro[1] * 0.01 * gro[3] + gro[1]) * gro[5])
                for line in f:
                    f1.write(line)
                f1.write(f'\n\t\t{self.current_date} {self.current_time}    {self.bill_number}')
                f1.write(f'\n\t\t-----------------------------------------------------------\n')
                for item in bill_list:
                    gross_price = (item[1] * 0.01 * item[3] + item[1])
                    f1.write(
                        f"\t\t{item[0][:10]}\t\t\t{item[4]}\t\t\t{gross_price:.2f}x{item[5]}\t\t{gross_price * item[5]:.2f}{item[4]}\n")
                f1.write(f'\t\t-----------------------------------------------------------\n')
                f1.write(f'\t\tSprzedaż opodatkowania A\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[0]:.2f}\n')
                f1.write(f'\t\tPTU A 23.00%\t\t\t\t\t\t\t\t\t{(self.sort.sort_ptu(bill_list)[0] * 0.23):.2f}\n')
                f1.write(f'\t\tSprzedaż opodatkowania B\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[1]:.2f}\n')
                f1.write(f'\t\tPTU B  8.00%\t\t\t\t\t\t\t\t\t{(self.sort.sort_ptu(bill_list)[1] * 0.08):.2f}\n')
                f1.write(f'\t\tSprzedaż opodatkowania C\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[2]:.2f}\n')
                f1.write(f'\t\tPTU C  5.00%\t\t\t\t\t\t\t\t\t{(self.sort.sort_ptu(bill_list)[2] * 0.05):.2f}\n')
                f1.write(f'\t\tSprzedaż opodatkowania D\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[3]:.2f}\n')
                f1.write(f'\t\tPTU D  0.00%\t\t\t\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[3]:.2f}\n')
                f1.write(f'\t\tSUMA netto: \t\t\t\t\t\t\t\t\t{sum(overall_net):.2f}')
                f1.write(f'\n\t\tSUMA brutto:\t\t\t\t\t\t\t\t\t{sum(overall_gross):.2f}')
                f1.write(f'\n\t\t-----------------------------------------------------------\n')

    def generate_invoice(self, order_file):
        with open('example_bill.txt') as f:
            with open(f"output_invoice_{self.timestamp}.txt", "w", encoding = 'utf-8') as f1:
                client_data = self.read_order(order_file)
                client_type = client_data[0]
                client_name = client_data[1]
                client_address = self.bill.add_client_to_bill(client_type, client_name)
                overall_net = []
                overall_gross = []
                bill_list = self.generate_list_from_order(order_file)
                for net in bill_list:
                    overall_net.append(net[1] * net[5])
                for gro in bill_list:
                    overall_gross.append((gro[1] * 0.01 * gro[3] + gro[1]) * gro[5])
                for line in f:
                    f1.write(line)
                f1.write(f'\n\t\t{self.current_date} {self.current_time}    {self.bill_number}')
                f1.write(f'\n\t\t-----------------------------------------------------------\n')
                f1.write(f'\t\tImię i Nazwisko: {client_name}\n')
                f1.write(f'\t\tMiasto: {client_address["miasto"]}\n')
                f1.write(f'\t\tKod pocztowy: {client_address["kod pocztowy"]}\n')
                f1.write(f'\t\tUlica: {client_address["ulica"]}\n')
                f1.write(f'\t\tNumer budynku: {client_address["numer budynku"]}\n')
                f1.write(f'\t\temail: {client_address["e-mail"]}\n')
                f1.write(f'\t\tNIP: {client_address["NIP"]}')
                f1.write(f'\n\t\t-----------------------------------------------------------\n')
                for item in bill_list:
                    gross_price = (item[1] * 0.01 * item[3] + item[1])
                    f1.write(
                        f"\t\t{item[0][:10]}\t\t\t{item[4]}\t\t\t{gross_price:.2f}x{item[5]}\t\t{gross_price * item[5]:.2f}{item[4]}\n")
                f1.write(f'\t\t-----------------------------------------------------------\n')
                f1.write(f'\t\tSprzedaż opodatkowania A\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[0]:.2f}\n')
                f1.write(f'\t\tPTU A 23.00%\t\t\t\t\t\t\t\t\t{(self.sort.sort_ptu(bill_list)[0] * 0.23):.2f}\n')
                f1.write(f'\t\tSprzedaż opodatkowania B\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[1]:.2f}\n')
                f1.write(f'\t\tPTU B  8.00%\t\t\t\t\t\t\t\t\t{(self.sort.sort_ptu(bill_list)[1] * 0.08):.2f}\n')
                f1.write(f'\t\tSprzedaż opodatkowania C\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[2]:.2f}\n')
                f1.write(f'\t\tPTU C  5.00%\t\t\t\t\t\t\t\t\t{(self.sort.sort_ptu(bill_list)[2] * 0.05):.2f}\n')
                f1.write(f'\t\tSprzedaż opodatkowania D\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[3]:.2f}\n')
                f1.write(f'\t\tPTU D  0.00%\t\t\t\t\t\t\t\t\t{self.sort.sort_ptu(bill_list)[3]:.2f}\n')
                f1.write(f'\t\tSUMA netto: \t\t\t\t\t\t\t\t\t{sum(overall_net):.2f}')
                f1.write(f'\n\t\tSUMA brutto:\t\t\t\t\t\t\t\t\t{sum(overall_gross):.2f}')
                f1.write(f'\n\t\t-----------------------------------------------------------\n')
                f1.write(f'\t\tData wystawienia: {str(datetime.now())[:19]}\n')
                f1.write(f'\t\tData sprzedaży: {str(datetime.now())[:19]}\n')
                f1.write(f'\t\tTermin płatności: {str(datetime.now() + timedelta(days=3))[:10]}')
                f1.write(f'\n\t\t-----------------------------------------------------------\n')


def main():
    project = Project()
    """
    Creating invoices doesn't work as intended, I messed up with logic and I am lost ;)
    """
    bill_type = 'I'  # B for generate bill, I for generate invoice
    order_file = 'order.csv'
    if bill_type == 'I':
        project.generate_invoice(order_file)
    elif bill_type == 'B':
        project.generate_bill(order_file)
    else:
        print("Select B for generate bill, I for generate invoice")


if __name__ == '__main__':
    main()
