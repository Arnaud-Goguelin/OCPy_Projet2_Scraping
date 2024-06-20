import csv

def export_data_in_csv(book):
    with open('book.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for key, value in book.items():
            writer.writerow([key, value])

