import sys
from lib.get_book_data import get_book_data
from lib.get_category_data import get_category_data
from lib.get_website_data import get_website_data
from lib.export_data import (
    export_category_books,
    export_one_book,
    export_website_books,
)
from lib.utils.get_time import get_time


def scrap_book(book_url):
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


def scrap_category(category_url):
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


def scrap_website():
    website_url = "http://books.toscrape.com/"  # give feed back in console
    starting_time = get_time()
    print(f"website scrappring begins at {starting_time}")

    books_from_website = get_website_data(website_url)
    export_website_books(books_from_website)

    # give feed back in console
    ending_time = get_time()
    print(
        f"website scrappring ends at {ending_time}\nIt took {ending_time - starting_time}\n\n"
    )


def start_scrapping():

    choice = input(
        "Choose what you want to scrap (book, category, website) or do you want to leave (leave)? "
    )
    if choice not in ["book", "category", "website", "leave"]:
        print("Invalid choice")
        start_scrapping()
    elif choice == "leave":
        print("Good bye")
        sys.exit(0)
    elif choice == "website":
        scrap_website()

    url = input("Enter an URL to scrap: ")

    if choice == "book":
        if "category" in url or "catalogue" not in url:
            print("Invalid URL for book scraping")
            sys.exit(1)
        else:
            scrap_book(url)
    elif choice == "category":
        if "category" not in url:
            print("Invalid URL for category scraping")
            sys.exit(1)
        else:
            scrap_category(url)
