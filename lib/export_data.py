import csv

def export_one_book_in_csv(book):
    with open('one_book.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for key, value in book.items():
            writer.writerow([key, value])

