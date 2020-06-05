import csv

with open('order_invoice.csv', newline = '') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ';')
    csv_headings = next(reader)
    first_line = next(reader)
    if 'Firmy' in first_line['Type']:
        print('Firmy')

# print(reader)
