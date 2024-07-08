from lib.get_book_data import get_book_data
from lib.get_category_data import get_category_data
from lib.get_website_data import get_website_data
from lib.export_data import (
    export_category_books,
    export_one_book,
    export_website_books,
)
from lib.utils.get_time import get_time

book_url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"
category_url = (
    "http://books.toscrape.com/catalogue/category/books/philosophy_7/index.html"
)
website_url = "http://books.toscrape.com/"

if __name__ == "__main__":

    # scrap one book
    # give feed back in console
    starting_time = get_time()
    print(f"one book scrappring begins at {starting_time}")

    book = get_book_data(book_url)
    export_one_book(book)

    # give feed back in console
    ending_time = get_time()
    print(
        f"one book scrappring ends at {ending_time}\nIt took {ending_time - starting_time}\n\n"
    )

    # scrap all books in one category
    # give feed back in console
    starting_time = get_time()
    print(f"one category scrappring begins at {starting_time}")

    books_from_category = get_category_data(category_url)
    export_category_books(books_from_category)

    # give feed back in console
    ending_time = get_time()
    print(
        f"one category scrappring ends at {ending_time}\nIt took {ending_time - starting_time}\n\n"
    )

    # scrap all books from website
    # give feed back in console
    starting_time = get_time()
    print(f"website scrappring begins at {starting_time}")

    books_from_website = get_website_data(website_url)
    export_website_books(books_from_website)

    # give feed back in console
    ending_time = get_time()
    print(
        f"website scrappring ends at {ending_time}\nIt took {ending_time - starting_time}\n\n"
    )
