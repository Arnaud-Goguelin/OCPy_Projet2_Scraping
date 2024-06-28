import datetime


from lib.get_html import get_html
from lib.get_data import (
    get_category_data,
    get_book_data,
    get_website_data,
)
from lib.export_datas import (
    export_category_books,
    export_one_book,
    export_website_books,
)

book_url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"
category_url = (
    "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
)
website_url = "http://books.toscrape.com/"

if __name__ == "__main__":

    print(f"scrap one book begins at {datetime.datetime.now()}")
    book_page = get_html(book_url)

    book = {}
    book["Book_page_url"] = book_url
    get_book_data(book_page, book_url, book)
    export_one_book(book)
    print(f"scrap one book ends at {datetime.datetime.now()}")

    print(f"scrap one category begins at {datetime.datetime.now()}")
    category_page = get_html(category_url)

    books_from_category = []
    get_category_data(category_page, category_url, books_from_category)
    export_category_books(books_from_category)
    print(f"scrap one category ends at {datetime.datetime.now()}")

    print(f"scrap website begins at {datetime.datetime.now()}")
    books_from_categories = []
    landing_page = get_html(website_url)
    get_website_data(landing_page, website_url, books_from_categories)
    export_website_books(books_from_categories)
    print(f"scrap website ends at {datetime.datetime.now()}")
