from lib.get_html import get_html
from lib.get_data import (
    get_category_data,
    get_book_data,
    get_website_data,
)
from lib.export_data import (
    export_category_books,
    export_one_book,
    export_website_books,
)
from lib.get_time import get_time

book_url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"
category_url = (
    "http://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html"
)
website_url = "http://books.toscrape.com/"

if __name__ == "__main__":

    # scrap one book
    print(f"one book scrappring begins at {get_time()}")
    book_page = get_html(book_url)

    book = get_book_data(book_page, book_url)
    book["Book_page_url"] = book_url
    export_one_book(book)
    print(f"one book scrappring ends at {get_time()}\n\n")

    # scrap all books in one category
    print(f"one category scrapping begins at {get_time()}")
    category_page = get_html(category_url)

    books_from_category = get_category_data(category_page, category_url)
    export_category_books(books_from_category)
    print(f"one category scrapping ends at {get_time()}\n\n")

    # scrap all books from website
    print(f"website scrapping begins at {get_time()}")
    landing_page = get_html(website_url)

    books_from_website = get_website_data(landing_page, website_url)
    export_website_books(books_from_website)
    print(f"website scrapping ends at {get_time()}")
