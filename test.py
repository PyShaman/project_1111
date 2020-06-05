import csv

with open('order.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        print(row['Type'], row['Client'], row['Category'], row['Subcategory'], row['id'], row['quantity'])

# print(reader)
