from lib.get_book_data import get_book_data
from lib.get_html import get_html
from lib.get_data import (
    get_category_data,
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

# ! scrapping du website: on obtient acutellement une liste de liste de dictionnaire, il nous faut juste une liste de dictionnaire

if __name__ == "__main__":

    # scrap one book
    starting_time = get_time()
    print(f"one book scrappring begins at {starting_time}")
    book_page = get_html(book_url)

    book = get_book_data(book_page, book_url)
    book["Book_page_url"] = book_url
    export_one_book(book)
    ending_time = get_time()
    print(f"one book scrappring ends at {ending_time}\nIt took {ending_time - starting_time}\n\n")

    # # scrap all books in one category
    # starting_time = get_time()
    # print(f"one category scrappring begins at {starting_time}")

    # category_page = get_html(category_url)

    # books_from_category = get_category_data(category_page, category_url)
    # export_category_books(books_from_category)
    # ending_time = get_time()
    # print(f"one category scrappring ends at {ending_time}\nIt took {ending_time - starting_time}\n\n")

    # scrap all books from website
    # starting_time = get_time()
    # print(f"website scrappring begins at {starting_time}")

    # landing_page = get_html(website_url)

    # books_from_website = get_website_data(landing_page, website_url)
    # export_website_books(books_from_website)
    # ending_time = get_time()
    # print(f"website scrappring ends at {ending_time}\nIt took {ending_time - starting_time}\n\n")
