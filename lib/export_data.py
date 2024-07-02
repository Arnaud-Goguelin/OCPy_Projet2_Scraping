import csv


# write datas from one book in one .csv file
def export_one_book(book):
    """
    write the given book's data in a .csv file

    Parameters:
    book (dictionnary Key(string) : Value(string)): the given book's data to be writtent in a .csv file

    Returns:
    create a .csv file where:
        headers are book's keys
        row are book's value
        delimiter is |

    Raises:
    none
    """
    with open("one_book.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=book.keys(), delimiter="|")
        writer.writeheader()
        writer.writerow(book)


# write datas from books in one category in one .csv file
def export_category_books(books):
    """
    write the given books' data from one category in a .csv file

    Parameters:
    books (list of 'book' dictionnary Key(string) : Value(string)):
        the given list of books' data to be written in a .csv file


    Returns:
    create a .csv file where:
        headers are book's keys
        row are book's value
        delimiter is |

    Raises:
    none
    """
    with open("books_from_category.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys(), delimiter="|")
        writer.writeheader()
        for book in books:
            writer.writerow(book)


# write datas from books from each category in one .csv file
# export_website_books is the same function as export_category_books
# it's just allow us to write datas in a different file for exercices purpose
def export_website_books(books_sorted_by_category):
    """
    write the given books' data from all categories in the website in a .csv file

    Parameters:
    books_sorted_by_category (list of list of 'book' dictionnary Key(string) : Value(string)):
        the given list of all categories
        wich are list of dictionnary
        containning books' data to be written in a .csv file

    Returns:
    create a .csv file where:
        headers are book's keys
        row are book's value
        delimiter is |

    Raises:
    none
    """
    with open("books_from_website.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=books_sorted_by_category[0][0].keys(), delimiter="|")
        writer.writeheader()
        for category in books_sorted_by_category:
            for book in category:
                writer.writerow(book)
