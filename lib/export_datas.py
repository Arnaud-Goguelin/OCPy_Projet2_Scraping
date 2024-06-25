import csv


# write datas from one book in one .csv file
def export_one_book(book):
    with open('one_book.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=book.keys(), delimiter='|')
        writer.writeheader()
        writer.writerow(book)


# write datas from books in one category in one .csv file
def export_category_books(books):
    with open('books_from_category.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys(), delimiter='|')
        writer.writeheader()
        for book in books:
            writer.writerow(book)


# write datas from books from each category in one .csv file
# export_website_books is the same function as export_category_books
# it's just allow us to write datas in a different file for exercices purpose
def export_website_books(books):
    with open('books_from_website.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys(), delimiter='|')
        writer.writeheader()
        for book in books:
            writer.writerow(book)
