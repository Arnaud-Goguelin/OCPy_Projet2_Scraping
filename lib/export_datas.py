import csv


def export_one_book(book):
    with open('one_book.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=book.keys(), delimiter='|')
        writer.writeheader()
        writer.writerow(book)


def export_category_books(books):
    with open('books_from_category.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys(), delimiter='|')
        writer.writeheader()
        for book in books:
            writer.writerow(book)
